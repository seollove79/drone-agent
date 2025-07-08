import asyncio
import websockets

clients = set()

async def relay(websocket):
    print("클라이언트 접속")
    clients.add(websocket)
    try:
        async for message in websocket:
            print("수신:", message)
            # 모든 다른 클라이언트에게 메시지 전달
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except Exception as e:
        print("연결 종료/에러:", e)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(relay, "localhost", 8111):
        print("[Relay WebSocket 서버] ws://localhost:8111 에서 대기 중...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())