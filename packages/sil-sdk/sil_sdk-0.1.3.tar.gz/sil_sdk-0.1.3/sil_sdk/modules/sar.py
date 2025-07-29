import asyncio
import websockets
import json
import threading


class SARModule:
    def __init__(self, server_uri="ws://localhost:8766"):
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
        asyncio.create_task(self._listen())  # Start background feedback listener

    async def _listen(self):
        while True:
            try:
                response = await self.websocket.recv()
                self.status = json.loads(response)
            except websockets.ConnectionClosed:
                print("[SAR] WebSocket disconnected. Reconnecting...")
                await self._connect()
                break

    def set_parameters(self, graspCommand=False, velocity=50, strokeMin=0, strokeMax=100,
                       maxContactForce=50, axialThreshold=50, lateralThreshold=50):
        message = {
            "graspCommand": graspCommand,
            "setVelocity": velocity,
            "strokeMin": strokeMin,
            "strokeMax": strokeMax,
            "setMaxContactForce": maxContactForce,
            "setAxialForceThreshold": axialThreshold,
            "setLateralForceThreshold": lateralThreshold
        }
        asyncio.run_coroutine_threadsafe(self.websocket.send(json.dumps(message)), self.loop)

    def get_current_status(self):
        return self.status

    def close(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
