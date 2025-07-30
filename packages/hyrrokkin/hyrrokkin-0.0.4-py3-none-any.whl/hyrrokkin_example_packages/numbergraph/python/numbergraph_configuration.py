#   Hyrrokkin - a library for building and running executable graphs
#
#   MIT License - Copyright (C) 2022-2025  Visual Topology Ltd

import pickle
import asyncio
import json

from hyrrokkin_engine.configuration_interface import ConfigurationInterface

from .number_display_node import NumberDisplayNode
from .prime_factors_node import PrimeFactorsNode
from .number_input_node import NumberInputNode

class NumbergraphConfiguration(ConfigurationInterface):

    def __init__(self, services):
        self.services = services
        self.client_services = {}
        self.prime_factor_cache = None
        self.last_save_cache_task = None

    async def load(self):
        cache_data = await self.services.get_data("prime_factors")
        self.prime_factor_cache = pickle.loads(cache_data) if cache_data else {}
        self.services.set_status(f"loaded cache ({len(self.prime_factor_cache)} items)","info")

    async def create_node(self, node_type_id, node_services):
        match node_type_id:
            case "number_display_node": return NumberDisplayNode(node_services)
            case "number_input_node": return NumberInputNode(node_services)
            case "prime_factors_node": return PrimeFactorsNode(node_services)
            case _: return None

    def update_clients(self):
        for id in self.client_services:
            self.client_services[id].send_message(len(self.prime_factor_cache))

    def get_prime_factors(self, n):
        if n in self.prime_factor_cache:
            return self.prime_factor_cache[n]
        else:
            return None

    async def save_cache(self):
        await self.services.set_data("prime_factors", pickle.dumps(self.prime_factor_cache))

    async def set_prime_factors(self, n, factors):
        self.prime_factor_cache[n] = factors
        await self.save_cache()
        self.update_clients()

    def open_client(self, session_id, client_id, client_options, client_service):
        self.client_services[session_id+":"+client_id] = client_service

        def message_handler(msg):
            if msg == "clear_cache":
                self.last_save_cache_task = asyncio.get_event_loop().create_task(self.save_cache())

        client_service.set_message_handler(message_handler)
        self.update_clients()

    # implement encode/decode for the link types defined in this package

    def encode(self, value, link_type):
        if link_type == "integer":
            v = str(value)
        elif link_type == "integerlist":
            v = list(map(lambda i: str(i), value))
        encoded_bytes = json.dumps(v).encode("utf-8")
        return encoded_bytes

    def decode(self, encoded_bytes, link_type):
        v = json.loads(encoded_bytes.decode("utf-8"))
        if link_type == "integer":
            return int(v)
        elif link_type == "integerlist":
            return list(map(lambda i: int(i), v))






