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
        self.response_queue = asyncio.Queue()

    async def connect(self):
        if self.websocket is None:
            self.websocket = await websockets.connect(self.server_uri)
            asyncio.create_task(self.listen_for_results())

    async def listen_for_results(self):
        while True:
            try:
                response = await self.websocket.recv()
                data = json.loads(response)

                if "image" in data:
                    img_base64 = data["image"]
                    try:
                        img_data = base64.b64decode(img_base64)
                        np_arr = np.frombuffer(img_data, np.uint8)
                        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                        data["image"] = img
                    except Exception as e:
                        print("[ERROR] Decoding image failed:", e)
                        data["image"] = None

                module_name = data.get("module", "unknown")

                # Ensure deep copy to avoid stale reference issues
                self.results[module_name] = copy.deepcopy(data)

                # Put in queue for any awaiters
                await self.response_queue.put(copy.deepcopy(data))

            except websockets.ConnectionClosed:
                print("[ERROR] WebSocket connection closed. Reconnecting...")
                self.websocket = None
                await asyncio.sleep(1)
                await self.connect()
            except Exception as e:
                print("[ERROR] Unexpected exception in result listener:", e)
                await asyncio.sleep(0.5)

    async def load_module(self, module_name):
        await self.connect()
        request = {"command": f"{module_name}_load"}
        await self.websocket.send(json.dumps(request))

    async def run_module(self, module_name, prompt=None, bbox=None, mask=None):
        await self.connect()
        request = {"command": f"{module_name}_run"}
        if prompt:
            request["prompt"] = prompt
        if bbox:
            request["bbox"] = bbox
        if mask is not None:
            _, buffer = cv2.imencode('.png', mask)
            request["mask"] = base64.b64encode(buffer).decode('utf-8')
        await self.websocket.send(json.dumps(request))

        while True:
            data = await self.response_queue.get()
            if data.get("module") == module_name:
                return data

    async def stop_module(self, module_name):
        await self.connect()
        request = {"command": f"{module_name}_stop"}
        await self.websocket.send(json.dumps(request))

    async def close(self):
        if self.websocket:
            await self.websocket.close()
