# fnsignal

간단하고 강력한 Python 시그널/이벤트 시스템

## 설치

```bash
pip install fnsignal
```

## 빠른 시작

### 1. 기본 사용법

```python
from fnsignal.fnsignal import signal_manager

# 콜백 함수 정의
def my_callback(signal_name, data, sender):
    print(f"시그널명: {signal_name}, 데이터: {data}, 보낸이: {sender}")

# 콜백 등록
signal_manager.register_callback("hello", my_callback)

# 시그널 발송
signal_manager.send_signal("hello", data={"foo": "bar"}, sender="나")
```

### 2. 여러 콜백 등록

```python
def cb1(signal_name, data, sender):
    print("cb1:", data)

def cb2(signal_name, data, sender):
    print("cb2:", data)

signal_manager.register_callback("event", cb1)
signal_manager.register_callback("event", cb2)
signal_manager.send_signal("event", 123, sender="user")
```

### 3. 콜백 해제

```python
signal_manager.unregister_callback("event", cb1)
signal_manager.send_signal("event", 456, sender="user")
```

### 4. 비동기 콜백

```python
import asyncio

async def async_cb(signal_name, data, sender):
    print("비동기 콜백:", data)

signal_manager.register_callback("async_event", async_cb)
signal_manager.send_signal("async_event", "async data", sender="user")
```

## 주요 기능

### 1. 시그널 관리
- 시그널 발송/수신
- 콜백 등록/해제
- 우선순위 기반 콜백 실행
- 필터 조건 지원

### 2. 비동기 지원
- 동기/비동기 콜백 모두 지원
- asyncio 이벤트 루프 자동 관리
- Thread-safe 설계

### 3. 통계 및 모니터링
- 시그널/콜백 실행 통계
- 에러 카운트 및 로깅
- 실행 시간 측정

### 4. 안전성
- 자동 에러 처리
- 연속 에러 시 자동 재초기화
- Thread-safe 동작

## API 문서

### signal_manager.register_callback(signal_name, callback, sender=None, priority=SignalPriority.NORMAL, filter_condition=None, stop_propagation=False)
- 시그널에 콜백을 등록합니다.
- 우선순위, 필터, 전파 중단 옵션 지정 가능

### signal_manager.unregister_callback(signal_name, callback)
- 특정 시그널의 콜백을 해제합니다.

### signal_manager.send_signal(signal_name, data=None, sender=None, priority=SignalPriority.NORMAL)
- 시그널을 발송합니다.
- 등록된 콜백들이 우선순위에 따라 실행됩니다.

### signal_manager.get_signal_stats()
- 현재 시그널 시스템의 통계 정보를 반환합니다.

## 라이선스

MIT License 