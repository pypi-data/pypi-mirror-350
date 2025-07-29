import asyncio
import websockets
import json
import threading


class DAGModule:
    def __init__(self, server_uri="ws://localhost:8767"):
        self.server_uri = server_uri
        self.websocket = None
        self.status = {}
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect())

    async def _connect(self):
        self.websocket = await websockets.connect(self.server_uri)
        asyncio.create_task(self._listen())  # Background listener

    async def _listen(self):
        while True:
            try:
                response = await self.websocket.recv()
                self.status = json.loads(response)
            except websockets.ConnectionClosed:
                print("[DAG] WebSocket disconnected. Reconnecting...")
                await self._connect()
                break

    def grasp(self, grasp_mode="pinch", velocity=75,
              pos_min=None, pos_max=None, max_contact_force=None):
        # Default joint configs if not provided
        default_pos = {f"joint_{i}": 10 for i in range(1, 13)}
        default_max = {f"joint_{i}": 80 for i in range(1, 13)}
        default_force = {f"joint_{i}": 50 for i in range(1, 13)}

        message = {
            "grasp_command": True,
            "enable_multi_grasp": False,
            "grasp_mode": grasp_mode,
            "pos_min": pos_min or default_pos,
            "pos_max": pos_max or default_max,
            "velocity": velocity,
            "max_contact_force": max_contact_force or default_force
        }
        asyncio.run_coroutine_threadsafe(self.websocket.send(json.dumps(message)), self.loop)

    def get_current_status(self):
        return self.status

    def close(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
