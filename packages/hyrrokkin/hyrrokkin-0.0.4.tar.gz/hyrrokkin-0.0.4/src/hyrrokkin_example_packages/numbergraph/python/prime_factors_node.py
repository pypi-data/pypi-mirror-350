#   Hyrrokkin - a library for building and running executable graphs
#
#   MIT License - Copyright (C) 2022-2025  Visual Topology Ltd


import asyncio
import sys
import json
import time

from hyrrokkin_engine.node_interface import NodeInterface

class PrimeFactorsNode(NodeInterface):

    def __init__(self,services):
        self.services = services
        self.sub_process = None

    def reset_run(self):
        if self.sub_process is not None:
            self.sub_process.terminate()

    async def run(self, inputs):
        start_time = time.time()
        n = inputs.get("data_in",None)
        if n is not None:
            self.services.set_status("calculating...", "info");
            if n < 2:
                raise Exception(f"input value {n} is invalid (< 2)")

            prime_factors = self.services.get_configuration().get_prime_factors(n)

            if not prime_factors:
                prime_factors = await self.find_prime_factors(n)

            elapsed_time_ms = int(1000*(time.time() - start_time))

            if prime_factors is not None:
                self.services.set_status(f"{elapsed_time_ms} ms", "info");
                await self.services.get_configuration().set_prime_factors(n, prime_factors)
                return { "data_out":prime_factors }
            else:
                self.services.set_status("Failed to calculate prime factors", "error");
                raise Exception("prime factors error")

    async def find_prime_factors(self,n):
        script_path = self.services.resolve_resource("python/prime_factors_worker.py").replace("file://", "")
        prime_factors = None
        try:
            self.sub_process = await asyncio.create_subprocess_exec(sys.executable, script_path, str(n),
                                                                   stdout=asyncio.subprocess.PIPE,
                                                                   stderr=asyncio.subprocess.PIPE)
            stdout, _ = await self.sub_process.communicate()
            prime_factors = json.loads(stdout.decode().strip("\n"))
        except:
            pass
        self.sub_process = None
        return prime_factors






