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

from .data_store_utils import DataStoreUtils

class InMemoryDataStoreUtils:

    def __init__(self, target_id, target_type):
        self.target_id = target_id
        self.target_type = target_type
        self.properties = {}
        self.data = {}

    async def load_properties(self):
        return self.properties

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties

    async def save_properties(self):
        pass

    def get_property(self, name, default_value):
        return self.properties.get(name, default_value)

    def set_property(self, name, value):
        self.properties[name] = value

    async def get_data(self, key):
        return self.get_data_sync(key)

    async def set_data(self, key, data):
        self.set_data_sync(key, data)

    def get_data_keys(self):
        return list(self.data.keys())

    def get_data_sync(self, key):
        DataStoreUtils.check_valid_data_key(key)
        if key in self.data:
            return self.data[key]
        return None

    def set_data_sync(self, key, data):
        DataStoreUtils.check_valid_data_key(key)
        DataStoreUtils.check_valid_data_value(data)
        self.data[key] = data


