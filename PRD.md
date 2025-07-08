# PRD: Raspberry Pi Drone Agent (WebSocket 기반)

## 목적
Pixhawk 기반 드론의 FC에 연결된 Raspberry Pi에서 pymavlink를 사용해 비행 데이터를 수집하고, WebSocket을 통해 지상 서버(관제 UI)와 실시간 통신하는 클라이언트 에이전트를 구현한다.

## 시스템 구성 개요
[Pixhawk]
  ↕ MAVLink (UART or USB)
[Raspberry Pi]
  ↕ WebSocket (Client)
[WebSocket 중계 서버]
  ↕
[Web UI]

## 디렉토리 구조
/drone-agent/
├── config/
│   └── config.yaml          # 설정 파일: FC 포트, WebSocket URL, 파라미터 등
├── mavlink/
│   └── fc_bridge.py         # pymavlink 기반 FC 연결 및 메시지 수신 처리
├── comms/
│   └── ws_client.py         # WebSocket client: 서버 연결 및 메시지 송수신
├── utils/
│   └── parser.py            # MAVLink 메시지 파싱 및 형식화
├── main.py                  # 전체 에이전트 실행 엔트리포인트
└── requirements.txt         # Python 패키지 목록

## 핵심 기능 요구사항

1. FC 통신 모듈 (fc_bridge.py)
- Pixhawk FC에 MAVLink 프로토콜로 연결
- 비행 상태, GPS, 모드, 배터리 등 주요 telemetry 수신
- FC 연결 재시도 로직 포함
- 특정 명령 (arm/disarm, set mode 등) 수신 시 FC에 전송

2. WebSocket 통신 모듈 (ws_client.py)
- 중계 서버에 WebSocket Client로 연결
- 연결 유지 (자동 reconnect), ping/pong 지원
- Telemetry 데이터 전송 (서버 → UI)
- 명령 수신 처리 (UI → 서버 → Pi)

3. 메시지 포맷 및 흐름
- MAVLink → 파싱 → JSON 변환 → WebSocket 송신
- WebSocket 수신 JSON → 파싱 → FC로 명령 전송

예시 송신 데이터:
{
  "drone_id": "drone_001",
  "type": "telemetry",
  "payload": {
    "mode": "GUIDED",
    "lat": 37.1234,
    "lon": 127.5678,
    "alt": 35.2,
    "battery": 89,
    "armed": true
  }
}

예시 수신 명령:
{
  "type": "command",
  "action": "set_mode",
  "value": "RTL"
}

## 설정 파일 (config.yaml) 예시
fc:
  device: /dev/ttyAMA0
  baudrate: 57600

websocket:
  url: wss://control-server.example.com/ws
  reconnect_interval: 5
  drone_id: drone_001

logging:
  level: INFO

## 예외 및 장애 처리
상황 | 처리 방식
------|-----------
FC 연결 실패 | 일정 시간 간격으로 재시도
WebSocket 끊김 | 재연결 로직 포함
잘못된 명령 수신 | 무시하고 로그 기록
MAVLink 메시지 오류 | 로그 기록 후 무시

## 유지 보수 및 확장성 고려
- 메시지 핸들러 분리로 다양한 FC 메시지 추가 수월
- drone_id 기반 다중 드론 식별 가능
- 향후 MQTT 등 타 통신 방식 추가 시 구조 확장 용이

## Python 의존성 (requirements.txt)
pymavlink>=2.4.20
websockets>=11.0
pyyaml

## 실행 방식
cd drone-agent
python main.py