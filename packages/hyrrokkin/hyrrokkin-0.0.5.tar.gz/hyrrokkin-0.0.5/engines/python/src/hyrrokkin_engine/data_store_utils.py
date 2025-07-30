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

import os
import json
import copy
import asyncio

class DataStoreUtils:

    def __init__(self, root_folder, target_id, target_type, read_only):
        self.root_folder = root_folder
        self.target_id = target_id
        self.target_type = target_type
        self.properties = {}
        self.data_cache = {}
        self.read_only = read_only

    def load_properties_sync(self):
        folder = os.path.join(self.root_folder, self.target_type, self.target_id)

        path = os.path.join(folder, "properties.json")
        if os.path.exists(path):
            with open(path) as f:
                self.properties = json.loads(f.read())
        else:
            self.properties = {}

    async def load_properties(self):
        self.load_properties_sync()

    @staticmethod
    def check_valid_data_key(key):
        for c in key:
            if not c.isalnum() and c != '_':
                raise ValueError("data key can only contain alphanumeric characters and underscores")

    @staticmethod
    def check_valid_data_value(data):
        if data is None:
            return True
        return isinstance(data, bytes)

    async def get_data(self, key):
        DataStoreUtils.check_valid_data_key(key)

        if key in self.data_cache:
            return self.data_cache[key]

        return await asyncio.to_thread(lambda k: self.__retrieve_data(k), key)

    def get_data_sync(self, key):
        DataStoreUtils.check_valid_data_key(key)

        if key in self.data_cache:
            return self.data_cache[key]

        return self.__retrieve_data(key)

    def __retrieve_data(self, key):
        filepath = os.path.join(self.root_folder, self.target_type, self.target_id, "data", key)

        if os.path.exists(filepath):
            with open(filepath, mode="rb") as f:
                return f.read()
        else:
            return None

    async def set_data(self, key, data):
        DataStoreUtils.check_valid_data_key(key)
        DataStoreUtils.check_valid_data_value(data)

        if self.read_only:
            self.data_cache[key] = data
        else:
            await asyncio.to_thread(lambda k, v: self.__store_data(k, v), key, data)

    def get_data_keys(self):
        raise NotImplementedError()

    def set_data_sync(self, key, data):
        DataStoreUtils.check_valid_data_key(key)
        DataStoreUtils.check_valid_data_value(data)

        if self.read_only:
            self.data_cache[key] = data
        else:
            self.__store_data(key, data)

    def __store_data(self, key, data):

        folder = os.path.join(self.root_folder, self.target_type, self.target_id, "data")

        filepath = os.path.join(folder, key)

        if data is None:
            if os.path.exists(filepath):
                os.remove(filepath)
            return

        os.makedirs(folder, exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(data)

    def save_properties(self):
        if self.read_only:
            return

        folder = os.path.join(self.root_folder, self.target_type, self.target_id)

        path = os.path.join(folder, "properties.json")

        os.makedirs(folder, exist_ok=True)
        with open(path,"w") as f:
            f.write(json.dumps(self.properties))

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = copy.deepcopy(properties)
        self.save_properties()

    def get_property(self, property_name, default_value=None):
        return self.properties.get(property_name, default_value)

    def set_property(self, property_name, property_value):
        if property_value is not None:
            self.properties[property_name] = property_value
        else:
            if property_name in self.properties:
                del self.properties[property_name]
        self.save_properties()



