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

import typing

from abc import abstractmethod
from typing import Union, Dict, List, Literal

JsonType = Union[Dict[str, "JsonType"], List["JsonType"], str, int, float, bool, None]

class NodeServiceInterface:

    @abstractmethod
    def resolve_resource(self, resource_path: str):
        """
        Resolve a relative resource path based on the location of the package schema

        Args:
            resource_path: the file path to resolve

        Returns:
            resolved path
        """
        pass

    """
    Defines a set of services that a node can access.
    """
    @abstractmethod
    def get_node_id(self) -> str:
        """
        Returns:
            a string containing the node's unique ID
        """
        pass

    @abstractmethod
    def set_status(self, status_message: str = "", level: Literal["info", "warning", "error"] = "info"):
        """
        Set an info status message for the node.

        Args:
            status_message: a short descriptive message or empty string (to clear the status)
            level: whether the message is "info", "warning" or "error"
        """
        pass

    @abstractmethod
    def set_execution_state(self, state:Literal["pending", "executing", "executed","failed"]):
        """
        Manually set the execution state of the node

        Args:
            state: one of "pending", "executing", "executed", "failed".

        Notes:
            Normally this is tracked by hyrrokkin, and nodes should not need to call this service.
            After making this call, the execution state will be tracked manually for the node involved.
        """
        pass

    @abstractmethod
    def request_run(self):
        """
        Request that this node be run
        """
        pass

    @abstractmethod
    def get_property(self, property_name: str, default_value: JsonType = None) -> JsonType:
        """
        Get the current value for the node's property

        Args:
            property_name: the name of the property
            default_value: a default value to return if the named property is not defined on the node

        Returns:
            the property value
        """
        pass

    @abstractmethod
    def set_property(self, property_name: str, property_value: JsonType):
        """
        Set the current value for the node's property

        Args:
            property_name: the name of the property
            property_value: the JSON-serialisable property value

        Notes:
            property values MUST be JSON-serialisable
        """
        pass

    @abstractmethod
    async def get_data(self, key: str) -> typing.Union[bytes, None]:
        """
        Get binary data (bytes) associated with this node.

        Args:
            key: a key to locate the data (can only contain alphanumeric characters and underscores)

        Returns:
            data or None if no data is associated with the key
        """
        pass

    @abstractmethod
    async def set_data(self, key: str, data: typing.Union[bytes, None]):
        """
        Set binary data (bytes) associated with this node.

        Args:
            key: a key to locate the data (can only contain alphanumeric characters and underscores)
            data: binary data (bytes) to be stored (or None to remove previously stored data for this key)
        """
        pass

    @abstractmethod
    def get_configuration(self, package_id: str = None) -> typing.Union[None, "configuruation_service_interface.ConfigurationServiceInterface"]:
        """
        Obtain a configuration object if defined for the node's package.

        Args:
            package_id: the id of the package configuration to obtain, or None to obtain the node's package configuration

        Returns:
            a configuration object or None
        """
        pass

    @abstractmethod
    def request_open_client(self, client_name: str, session_id: str=None):
        """
        Called to request that a client of this node be opened

        Args:
            client_name: the type of client to load
            session_id: specify which session to send the request to (defaults to all sessions)
        """
        pass










