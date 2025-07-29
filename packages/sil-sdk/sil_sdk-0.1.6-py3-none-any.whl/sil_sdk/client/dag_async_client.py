# dag_async_client.py

import asyncio
import json
import websockets

class DAGAsyncClient:
    def __init__(self, server_uri="ws://<server-ip>:8767"):
        self.server_uri = server_uri
        self.websocket = None
        self.response_queue = asyncio.Queue()

    async def connect(self):
        if self.websocket is None:
            self.websocket = await websockets.connect(self.server_uri)
            asyncio.create_task(self.listen_for_responses())

    async def listen_for_responses(self):
        while True:
            try:
                response = await self.websocket.recv()
                data = json.loads(response)
                await self.response_queue.put(data)
            except websockets.ConnectionClosed:
                print("DAG connection lost. Reconnecting...")
                self.websocket = None
                await self.connect()
                break

    async def send_command(self, command):
        await self.connect()
        await self.websocket.send(json.dumps(command))

    async def get_response(self):
        return await self.response_queue.get()

    async def close(self):
        if self.websocket:
            await self.websocket.close()
