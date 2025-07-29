import asyncio
from threading import Thread
import websockets
import cv2
import numpy as np
import base64
import json
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
            self._run_async_task(self._start_websocket_server()).result()
        self.client = VISAsyncClient(server_uri)

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run_async_task(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    async def _start_websocket_server(self):
        async def handler(websocket, path):
            try:
                async for message in websocket:
                    request = json.loads(message)
                    cmd = request.get("command")

                    if cmd == "obj_detection_load":
                        await asyncio.sleep(1)
                        await websocket.send(json.dumps({"status": "loaded", "module": "obj_detection"}))

                    elif cmd == "obj_detection_run":
                        await asyncio.sleep(1)
                        dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
                        _, buffer = cv2.imencode('.jpg', dummy_img)
                        img_base64 = base64.b64encode(buffer).decode("utf-8")
                        await websocket.send(json.dumps({
                            "status": "done",
                            "module": "obj_detection",
                            "image": img_base64,
                            "objects": [{"label": "dummy", "box": [10, 10, 50, 50]}]
                        }))

                    elif cmd == "obj_detection_stop":
                        await websocket.send(json.dumps({"status": "stopped", "module": "obj_detection"}))

            except websockets.ConnectionClosed:
                pass

        host, port = self._parse_uri(self.server_uri)
        self.ws_server = await websockets.serve(handler, host, port)

    def _parse_uri(self, uri):
        uri = uri.replace("ws://", "")
        if "/" in uri:
            uri = uri.split("/", 1)[0]
        host, port = uri.split(":")
        return host, int(port)

    def load(self, modules):
        for module in modules:
            self._run_async_task(self.client.load_module(module)).result()

    def run(self, module, prompt=None, bbox=None, mask=None):
        if module in self.running_tasks:
            return
        task = self._run_async_task(self._run_and_store_result(module, prompt, bbox, mask))
        self.running_tasks[module] = task

    async def _run_and_store_result(self, module, prompt, bbox, mask):
        result = await self.client.run_module(module, prompt, bbox, mask)
        self.results[module] = result

    def get_result(self, module):
        return self.results.get(module)

    def stop_all(self):
        for module in list(self.running_tasks.keys()):
            self._run_async_task(self.client.stop_module(module)).result()
        self.running_tasks.clear()

    def close(self):
        self.stop_all()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self._run_async_task(self.client.close()).result()
