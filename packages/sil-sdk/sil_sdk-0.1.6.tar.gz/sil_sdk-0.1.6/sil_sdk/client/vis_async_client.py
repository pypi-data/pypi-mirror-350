import asyncio
import json
import websockets
import cv2
import base64
import numpy as np
import copy

class VISAsyncClient:
    def __init__(self, server_uri="ws://localhost:4201"):
        self.server_uri = server_uri
        self.websocket = None
        self.results = {}
        self.response_queue = None

    async def connect(self):
        if self.websocket is None:
            self.websocket = await websockets.connect(self.server_uri)
            self.response_queue = asyncio.Queue()
            asyncio.create_task(self.listen_for_results())

    async def listen_for_results(self):
        while True:
            try:
                raw = await self.websocket.recv()
                data = json.loads(raw)

                # Decode image if present
                if "image" in data:
                    try:
                        arr = np.frombuffer(base64.b64decode(data["image"]), np.uint8)
                        data["image"] = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                    except Exception as e:
                        print("[ERROR] Decoding image:", e)
                        data["image"] = None

                module = data.get("module", "unknown")
                self.results[module] = copy.deepcopy(data)
                await self.response_queue.put(copy.deepcopy(data))

            except websockets.ConnectionClosed:
                self.websocket = None
                await asyncio.sleep(1)
                await self.connect()
            except Exception as e:
                print("[ERROR] listen_for_results:", e)
                await asyncio.sleep(0.1)

    async def load_module(self, module_name: str):
        await self.connect()
        await self.websocket.send(json.dumps({"command": f"{module_name}_load"}))

    async def run_module(self, module_name: str, prompt=None, bbox=None, mask=None):
        await self.connect()
        # flush old messages
        while not self.response_queue.empty():
            self.response_queue.get_nowait()

        req = {"command": f"{module_name}_run"}
        if prompt: req["prompt"] = prompt
        if bbox:   req["bbox"]   = bbox
        if mask is not None:
            _, buf = cv2.imencode('.png', mask)
            req["mask"] = base64.b64encode(buf).decode('utf-8')
        await self.websocket.send(json.dumps(req))

        # wait for first inference result
        while True:
            data = await self.response_queue.get()
            if data.get("module") == module_name and "image" in data:
                return data

    async def stop_module(self, module_name: str):
        await self.connect()
        await self.websocket.send(json.dumps({"command": f"{module_name}_stop"}))

    async def unload_module(self, module_name: str):
        await self.connect()
        await self.websocket.send(json.dumps({"command": f"{module_name}_unload"}))
        # wait for unload confirmation
        while True:
            msg = await self.response_queue.get()
            if msg.get("module") == module_name and msg.get("status") in ("success","error"):
                return msg

    async def close(self):
        if self.websocket:
            await self.websocket.close()
