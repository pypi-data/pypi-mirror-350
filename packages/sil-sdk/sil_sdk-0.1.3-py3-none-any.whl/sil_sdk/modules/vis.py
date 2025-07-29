import asyncio
from threading import Thread
from sil_sdk.client.vis_async_client import VISAsyncClient

class VISModule:
    def __init__(self, server_uri="ws://localhost:4201", start_server=True):
        self.server_uri = server_uri
        self.loop = asyncio.new_event_loop()
        self.results = {}
        self.running_tasks = {}
        self.background_thread = Thread(target=self._start_loop, daemon=True)
        self.background_thread.start()

        if start_server:
            # Optionally start internal server – your project skips this
            pass

        self.client = VISAsyncClient(server_uri)
        # Force connect and start listen loop
        self._run_async_task(self.client.connect()).result()

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run_async_task(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def load(self, modules):
        for module in modules:
            self._run_async_task(self.client.load_module(module)).result()

    def run(self, module, prompt=None, bbox=None, mask=None):
        if module in self.running_tasks:
            return
        task = self._run_async_task(self._run_and_store_result(module, prompt, bbox, mask))
        self.running_tasks[module] = task

    async def _run_and_store_result(self, module, prompt, bbox, mask):
        await self.client.run_module(module, prompt, bbox, mask)

    def get_result(self, module):
        return self.client.results.get(module)

    def stop_all(self):
        for module in list(self.running_tasks.keys()):
            self._run_async_task(self.client.stop_module(module)).result()
        self.running_tasks.clear()

    def close(self):
        self.stop_all()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self._run_async_task(self.client.close()).result()
