import time
from pymavlink import mavutil

class FCBridge:
    def __init__(self, device, baudrate=None):
        self.device = device
        self.baudrate = baudrate
        self.vehicle = None

    def connect(self):
        while True:
            try:
                if self.device.startswith('tcp:'):
                    # 예: tcp:127.0.0.1:5760
                    self.vehicle = mavutil.mavlink_connection(self.device)
                    self.vehicle.wait_heartbeat()
                    print(f"TCP로 FC에 연결됨: {self.device}")
                else:
                    self.vehicle = mavutil.mavlink_connection(self.device, baud=self.baudrate)
                    self.vehicle.wait_heartbeat()
                    print(f"시리얼로 FC에 연결됨: {self.device}")
                break
            except Exception as e:
                print(f"FC 연결 실패: {e}. 5초 후 재시도...")
                time.sleep(5)

    def disconnect(self):
        if self.vehicle:
            self.vehicle.close()
            self.vehicle = None
            print("FC 연결 해제")

    def request_data_stream(self, rate, start_stop=1):
        self.vehicle.mav.request_data_stream_send(
            self.vehicle.target_system,
            self.vehicle.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            rate,
            start_stop
        )

    def test(self):
        while True:
            message = self.vehicle.recv_match(blocking=True)
            if ((message.get_type() == 'HEARTBEAT' and message.type == 2)):
                print(message)

            if (message.get_type() == 'GLOBAL_POSITION_INT'):
                lat = message.lat / 1e7
                lon = message.lon / 1e7
                relative_alt = message.relative_alt / 1000.0
                vx = message.vx / 100.0
                vy = message.vy / 100.0
                vz = message.vz / 100.0
                heading = message.hdg / 100.0
                print(f"위치: ({lat}, {lon}), 고도: {relative_alt}m, 속도: ({vx}, {vy}, {vz}) m/s, 방향: {heading}°")

    def receive(self):
        if not self.vehicle:
            self.connect()
        while True:
            msg = self.vehicle.recv_match(blocking=True, timeout=1)
            if msg:
                yield msg.to_dict()

    def send_command(self, command, params=None):
        if not self.vehicle:
            self.connect()
        if command == 'arm':
            # params: { 'arm': True/False }
            if params and params.get('arm', True):
                arm_flag = 1
            else:
                arm_flag = 0
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0,
                arm_flag, 0, 0, 0, 0, 0, 0
            )
            print(f"{'ARM' if arm_flag else 'DISARM'} 명령 전송 완료")
        # 추후 set_mode 등 다른 명령 추가 가능 