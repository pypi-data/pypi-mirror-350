#   Hyrrokkin - a library for building and running executable graphs
#
#   MIT License - Copyright (C) 2022-2025  Visual Topology Ltd

import json

from hyrrokkin_engine.node_interface import NodeInterface

class NumberDisplayNode(NodeInterface):

    def __init__(self, services):
        self.services = services
        self.clients = {}
        self.input_values = []

    def update_status(self):
        self.services.set_status(f"{len(self.input_values)} list(s)")

    def reset_run(self):
        self.input_values = []
        self.update_status()
        for client_service in self.clients.values():
            client_service.send_message(self.input_values)

    async def run(self, inputs):
        self.input_values = []
        for input_value in inputs.get("data_in",[]):
            self.input_values.append(list(map(lambda n: str(n),input_value)))
        self.update_status()
        for (id,client_service) in self.clients.items():
            client_service.send_message(self.input_values)
        self.services.request_open_client("default")

    def open_client(self, session_id, client_name, client_options, client_service):
        self.clients[(session_id,client_name)] = client_service
        client_service.send_message(self.input_values)

    def close_client(self, session_id, client_name):
        del self.clients[(session_id, client_name)]



