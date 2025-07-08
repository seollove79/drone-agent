import asyncio
import websockets
import json

class WSClient:
    def __init__(self, url, drone_id):
        self.url = url
        self.drone_id = drone_id
        self.ws = None

    async def connect(self):
        while True:
            try:
                self.ws = await websockets.connect(self.url, ping_interval=20)
                print(f"WebSocket 서버에 연결됨: {self.url}")
                return
            except Exception as e:
                print(f"WebSocket 연결 실패: {e}. 5초 후 재시도...")
                await asyncio.sleep(5)

    async def send(self, data):
        if self.ws:
            await self.ws.send(json.dumps(data))

    async def receive(self):
        if self.ws:
            async for message in self.ws:
                yield json.loads(message) 