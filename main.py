import yaml
import asyncio
from mavlink.fc_bridge import FCBridge
from comms.ws_client import WSClient
from utils.parser import mavlink_to_json

with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

fc_conf = config['fc']
ws_conf = config['websocket']

def run():
    fc = FCBridge(fc_conf['device'], fc_conf['baudrate'])
    #ws = WSClient(ws_conf['url'], ws_conf['drone_id'])

    fc.connect()
    fc.request_data_stream(2,1)  # 1Hz 데이터 스트림 요청
    fc.test()  # 연결 테스트




    # async def telemetry_sender():
    #     for msg in fc.receive():
    #         data = {
    #             "drone_id": ws_conf['drone_id'],
    #             "type": "telemetry",
    #             "payload": mavlink_to_json(msg)
    #         }
    #         await ws.send(data)

    # async def command_receiver():
    #     async for msg in ws.receive():
    #         if msg.get("type") == "command":
    #             if msg.get("action") == "arm":
    #                 fc.send_command("arm", {"arm": msg.get("value", True)})
    #             # set_mode 등 다른 명령도 여기에 추가 가능

    # async def main_loop():
    #     await ws.connect()
    #     await asyncio.gather(
    #         telemetry_sender(),
    #         command_receiver()
    #     )

    # asyncio.run(main_loop())

if __name__ == '__main__':
    run() 