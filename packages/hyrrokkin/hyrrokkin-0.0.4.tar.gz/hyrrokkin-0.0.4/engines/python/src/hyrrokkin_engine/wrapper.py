#   Hyrrokkin - a library for building and running executable graphs
#
#   MIT License - Copyright (C) 2022-2025  Visual Topology Ltd
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
from importlib import import_module

from hyrrokkin_engine.client_service import ClientService

class Wrapper:

    def __init__(self, datastore_utils, services, send_message_cb, request_open_client_cb):
        self.datastore_utils = datastore_utils
        self.instance = None
        self.client_services = {}
        self.services = services
        self.services.set_wrapper(self)
        self.logger = logging.getLogger("NodeWrapper")
        self.send_message_cb = send_message_cb
        self.request_open_client_cb = request_open_client_cb

    def get_id(self):
        # override in subclass
        raise NotImplementedError()

    def get_type(self):
        # override in subclass
        raise NotImplementedError()

    def set_instance(self, instance):
        self.instance = instance

    def get_instance(self):
        return self.instance

    async def load_properties(self):
        await self.datastore_utils.load_properties()

    def get_property(self, property_name, default_value):
        return self.datastore_utils.get_property(property_name, default_value)

    def set_property(self, property_name, property_value):
        self.datastore_utils.set_property(property_name, property_value)

    def set_properties(self, properties):
        self.datastore_utils.set_properties(properties)

    async def get_data(self, key):
        return await self.datastore_utils.get_data(key)

    async def set_data(self, key, data):
        await self.datastore_utils.set_data(key, data)

    def request_open_client(self, client_name, session_id):
        if self.request_open_client_cb:
            self.request_open_client_cb(client_name, session_id)

    def open_client(self, session_id, client_name, client_options):

        def message_forwarder(*message_parts):
            # send a message to a client
            self.send_message_cb(session_id, client_name, *message_parts)
        try:
            if hasattr(self.instance, "open_client"):
                client_service = ClientService()
                client_service.open(message_forwarder)
                self.client_services[(session_id,client_name)] = client_service
                self.instance.open_client(session_id, client_name, client_options, client_service)
        except:
            self.logger.exception(f"Error in open_client for {str(self)}")

    def recv_message(self, session_id, client_name, *message):
        key = (session_id, client_name)
        if key in self.client_services:
            self.client_services[key].handle_message(*message)

    def close_client(self, session_id, client_name):
        key = (session_id, client_name)
        if key in self.client_services:
            client_service = self.client_services[key]
            client_service.close()
            try:
                if hasattr(self.instance, "close_client"):
                    self.instance.close_client(session_id, client_name)
            except:
                self.logger.exception(f"Error in close_client for {str(self)}")
            del self.client_services[key]

    @staticmethod
    def get_class(module_class_name):
        module_path, class_name = module_class_name.rsplit('.', 1)
        module = import_module(module_path)
        cls = getattr(module, class_name)
        return cls

