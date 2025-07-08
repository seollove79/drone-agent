def mavlink_to_json(msg):
    if msg is None:
        return None
    return msg

# 추후 메시지 타입별로 파싱/가공 로직 추가 가능 