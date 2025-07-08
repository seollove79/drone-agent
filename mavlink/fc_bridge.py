import time
from pymavlink import mavutil

class FCBridge:
    def __init__(self, device, baudrate=None):
        self.device = device
        self.baudrate = baudrate
        self.master = None

    def connect(self):
        while True:
            try:
                if self.device.startswith('tcp:'):
                    # 예: tcp:127.0.0.1:5760
                    self.master = mavutil.mavlink_connection(self.device)
                    print(f"TCP로 FC에 연결됨: {self.device}")
                else:
                    self.master = mavutil.mavlink_connection(self.device, baud=self.baudrate)
                    print(f"시리얼로 FC에 연결됨: {self.device}")
                break
            except Exception as e:
                print(f"FC 연결 실패: {e}. 5초 후 재시도...")
                time.sleep(5)

    def receive(self):
        if not self.master:
            self.connect()
        while True:
            msg = self.master.recv_match(blocking=True, timeout=1)
            if msg:
                yield msg.to_dict()

    def send_command(self, command, params=None):
        if not self.master:
            self.connect()
        if command == 'arm':
            # params: { 'arm': True/False }
            arm_flag = 1 if params and params.get('arm', True) else 0
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0,
                arm_flag, 0, 0, 0, 0, 0, 0
            )
            print(f"{'ARM' if arm_flag else 'DISARM'} 명령 전송 완료")
        # 추후 set_mode 등 다른 명령 추가 가능 