import time
import asyncio
import threading
import os
import logging
import sys
import traceback
import queue
import concurrent.futures
import atexit
import inspect
from typing import Optional, Callable, Dict, Set, List, Any, Union, Tuple
from contextlib import contextmanager
from functools import wraps
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from collections import defaultdict
import queue

# 로깅 설정
def setup_logging(
    level: int = logging.INFO,
    log_file: str = 'fnsignal.log',
    enable_console: bool = False,
    enable_file: bool = True,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """
    로깅 설정을 구성합니다.
    
    Args:
        level (int): 로깅 레벨
        log_file (str): 로그 파일 경로
        enable_console (bool): 콘솔 출력 활성화 여부
        enable_file (bool): 파일 출력 활성화 여부
        format_str (str): 로그 포맷 문자열
    """
    handlers = []
    
    if enable_console:
        handlers.append(logging.StreamHandler(sys.stdout))
    if enable_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    )

# 기본 로깅 설정
setup_logging()
logger = logging.getLogger(__name__)

class SignalPriority(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()

@dataclass
class SignalCallback:
    callback: Callable
    sender: Optional[str]
    priority: SignalPriority
    is_async: bool
    filter_condition: Optional[Callable[[Any], bool]]
    tags: Set[str] = field(default_factory=set)
    group: Optional[str] = None
    channel: Optional[str] = None
    stop_propagation: bool = False
    registered_at: datetime = field(default_factory=datetime.now)
    execution_count: int = 0
    total_execution_time: float = 0.0
    max_execution_time: float = 0.0
    error_count: int = 0
    
    def update_stats(self, execution_time: float, error: bool = False) -> None:
        self.execution_count += 1
        self.total_execution_time += execution_time
        self.max_execution_time = max(self.max_execution_time, execution_time)
        if error:
            self.error_count += 1
    
    @property
    def average_execution_time(self) -> float:
        return self.total_execution_time / self.execution_count if self.execution_count > 0 else 0.0
    
    @property
    def error_rate(self) -> float:
        return self.error_count / self.execution_count if self.execution_count > 0 else 0.0

@dataclass
class SignalStats:
    total_signals: int = 0
    active_callbacks: int = 0
    last_signal_time: Optional[datetime] = None
    signal_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    error_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    execution_times: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    total_execution_time: float = 0.0
    max_execution_time: float = 0.0
    
    def update_execution_time(self, execution_time: float) -> None:
        self.total_execution_time += execution_time
        self.max_execution_time = max(self.max_execution_time, execution_time)
    
    @property
    def average_execution_time(self) -> float:
        return self.total_execution_time / self.total_signals if self.total_signals > 0 else 0.0

class SignalManager:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    _event_loop = None
    _event_loop_lock = threading.Lock()
    _thread_local = threading.local()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._callbacks: Dict[str, List[SignalCallback]] = defaultdict(list)
                    self._tag_index: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)
                    self._group_index: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)
                    self._channel_index: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)
                    self._stats = SignalStats()
                    self._signal_queue = queue.PriorityQueue()
                    self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
                    self._running = True
                    self._print_lock = threading.Lock()
                    self._callback_locks: Dict[str, threading.Lock] = defaultdict(threading.Lock)
                    
                    # 무한 대기 관련 추가
                    self._infinite_wait_signals = set()
                    self._shutdown_called = False
                    
                    # 종료 시 검사 함수 등록
                    atexit.register(self._check_shutdown)
                    
                    # 메인 이벤트 루프 생성 및 별도 스레드에서 실행
                    self._event_loop = asyncio.new_event_loop()
                    def start_loop(loop):
                        asyncio.set_event_loop(loop)
                        loop.run_forever()
                    self._event_loop_thread = threading.Thread(target=start_loop, args=(self._event_loop,), daemon=True)
                    self._event_loop_thread.start()
                    
                    # 시그널 처리 스레드 시작
                    self._processing_thread = threading.Thread(target=self._process_signals, daemon=True)
                    self._processing_thread.start()
                    self._initialized = True

    def _check_shutdown(self):
        """프로그램 종료 시 호출되어 무한 대기 시그널과 shutdown 호출 여부를 확인"""
        if self._infinite_wait_signals and not self._shutdown_called:
            signals = ", ".join(self._infinite_wait_signals)
            logger.error(f"프로그램이 종료되었지만 shutdown()이 호출되지 않았습니다. 무한 대기 중인 시그널: {signals}")
            logger.error("메모리 누수와 스레드 누수를 방지하려면 프로그램 종료 전 signal_manager.shutdown()을 호출하세요.")
            # sys.stderr에도 출력
            print(f"[심각한 오류] shutdown()이 호출되지 않았습니다! 무한 대기 중인 시그널: {signals}", file=sys.stderr)
            print("메모리 누수와 스레드 누수를 방지하려면 프로그램 종료 전 signal_manager.shutdown()을 호출하세요.", file=sys.stderr)
            
            # 예비 셧다운 실행 - 메모리 누수 방지
            self._emergency_shutdown()
    
    def _emergency_shutdown(self):
        """
        예비 셧다운 - shutdown()이 호출되지 않았을 때 자동으로 리소스를 정리
        """
        logger.warning("예비 셧다운 메커니즘 실행 중... 리소스 정리를 시도합니다.")
        print("[경고] 예비 셧다운 메커니즘이 실행되고 있습니다. 올바른 사용법은 프로그램 종료 전 명시적으로 signal_manager.shutdown()을 호출하는 것입니다.", file=sys.stderr)
        
        try:
            # 1. 무한 대기 시그널의 이벤트 강제 설정하여 스레드 종료
            for signal_name in list(self._infinite_wait_signals):
                try:
                    # 해당 시그널의 모든 핸들러에 빈 데이터 전송
                    self.send_signal(signal_name, data="[예비 셧다운에 의해 강제 종료됨]", priority=SignalPriority.CRITICAL)
                    logger.warning(f"시그널 '{signal_name}'의 무한 대기를 강제 종료했습니다.")
                except Exception as e:
                    logger.error(f"시그널 '{signal_name}' 강제 종료 중 오류 발생: {e}")
            
            # 2. 모든 콜백 제거
            with self._lock:
                self._callbacks.clear()
                self._tag_index.clear()
                self._group_index.clear()
                self._channel_index.clear()
                self._infinite_wait_signals.clear()
            
            # 3. 이벤트 루프 종료
            if self._event_loop and self._event_loop.is_running():
                try:
                    self._event_loop.call_soon_threadsafe(self._event_loop.stop)
                except Exception as e:
                    logger.error(f"이벤트 루프 종료 중 오류 발생: {e}")
            
            # 4. 스레드 종료
            self._running = False
            
            # 5. 실행자 셧다운
            try:
                self._executor.shutdown(wait=False)  # 대기 없이 종료
            except Exception as e:
                logger.error(f"실행자 종료 중 오류 발생: {e}")
            
            logger.warning("예비 셧다운 완료. 일부 리소스는 여전히 정리되지 않았을 수 있습니다.")
            print("[정보] 예비 셧다운이 완료되었습니다. 최적의 리소스 정리를 위해 항상 명시적으로 shutdown()을 호출하세요.", file=sys.stderr)
            
        except Exception as e:
            logger.error(f"예비 셧다운 중 예상치 못한 오류 발생: {e}")
            logger.error(traceback.format_exc())

    def _process_signals(self):
        """시그널 처리 메인 루프"""
        # 이벤트 루프 설정
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while self._running:
            try:
                priority_value, signal_data = self._signal_queue.get(timeout=0.1)
                signal_name, data, sender, tags, group, channel = signal_data
                
                # 각 시그널에 대한 락 획득
                with self._callback_locks[signal_name]:
                    # 이벤트 루프에서 콜백 실행
                    future = asyncio.run_coroutine_threadsafe(
                        self._execute_callbacks(signal_name, data, sender, tags, group, channel),
                        self._event_loop
                    )
                    try:
                        # 콜백 실행 완료 대기
                        future.result(timeout=30)  # 30초 타임아웃
                        self._stats.total_signals += 1
                        self._stats.signal_counts[signal_name] += 1
                        self._stats.last_signal_time = datetime.now()
                    except concurrent.futures.TimeoutError:
                        logger.error(f"시그널 처리 타임아웃: {signal_name}")
                    except Exception as e:
                        logger.error(f"시그널 처리 오류: {e}")
                        logger.error(traceback.format_exc())
                
                self._signal_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"시그널 처리 오류: {e}")
                logger.error(traceback.format_exc())
        
        # 이벤트 루프 정리
        loop.close()

    async def _execute_callbacks(self, signal_name: str, data: Any, sender: Any, tags: Set[str], group: str, channel: str):
        """콜백 실행을 위한 비동기 메서드"""
        logger.info(f"시그널 '{signal_name}' 처리 시작 - 데이터: {data}")
        
        # 콜백 목록의 안전한 복사본 생성 및 정렬
        with self._lock:
            callbacks = [
                callback for callback in self._callbacks.get(signal_name, [])
                if (callback.sender is None or callback.sender == sender) and
                   (not tags or callback.tags.intersection(tags)) and
                   (not group or callback.group == group) and
                   (not channel or callback.channel == channel)
            ]
            
            if not callbacks:
                logger.warning(f"시그널 '{signal_name}'에 대한 일치하는 콜백이 없습니다.")
                return
                
            logger.info(f"시그널 '{signal_name}'에 대해 실행할 콜백 수: {len(callbacks)}")
            
            # 우선순위에 따라 정렬
            callbacks.sort(key=lambda x: {
                SignalPriority.LOW: 3,
                SignalPriority.NORMAL: 2,
                SignalPriority.HIGH: 1,
                SignalPriority.CRITICAL: 0
            }[x.priority])

        # 각 콜백 실행
        for callback in callbacks:
            try:
                logger.info(f"콜백 실행 시도: {callback.callback.__name__} (is_async={callback.is_async})")
                start_time = time.time()
                
                if callback.is_async:
                    # 비동기 콜백 실행
                    result = await callback.callback(signal_name, data, sender)
                else:
                    # 동기 콜백 실행
                    result = callback.callback(signal_name, data, sender)
                
                execution_time = time.time() - start_time
                callback.update_stats(execution_time)
                self._stats.update_execution_time(execution_time)
                logger.info(f"콜백 실행 완료: {callback.callback.__name__} - 실행 시간: {execution_time:.3f}초")
                
                if callback.stop_propagation:
                    logger.info("시그널 전파 중단")
                    break
                    
            except Exception as e:
                logger.error(f"콜백 실행 오류: {e}")
                logger.error(traceback.format_exc())
                callback.update_stats(0, error=True)
                self._stats.error_counts[signal_name] += 1

    def _update_index(self, index_dict: Dict[str, Set[Tuple[str, int]]], key: str, signal_name: str, callback_index: int, add: bool = True):
        """인덱스 업데이트를 위한 헬퍼 메서드"""
        if add:
            index_dict[key].add((signal_name, callback_index))
        else:
            index_dict[key].discard((signal_name, callback_index))
            # 빈 세트 제거
            if not index_dict[key]:
                del index_dict[key]

    def _remove_from_index(self, index_dict: Dict[str, Set[Tuple[str, int]]], signal_name: str, indices: Set[int]):
        """인덱스에서 항목 제거를 위한 헬퍼 메서드"""
        keys_to_remove = set()
        for key, entries in index_dict.items():
            # 제거할 항목 찾기
            to_remove = {(signal_name, idx) for idx in indices if (signal_name, idx) in entries}
            if to_remove:
                entries -= to_remove
                if not entries:  # 빈 세트인 경우
                    keys_to_remove.add(key)
        
        # 빈 세트 제거
        for key in keys_to_remove:
            del index_dict[key]

    def register_callback(
        self,
        signal_name: str,
        callback: Callable,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL,
        filter_condition: Optional[Callable] = None,
        tags: Set[str] = None,
        group: Optional[str] = None,
        channel: Optional[str] = None,
        stop_propagation: bool = False,
        is_async: Optional[bool] = None,
    ):
        """콜백 등록 (스레드 안전)"""
        with self._lock:
            # 타입 검증 추가
            if tags is not None and not isinstance(tags, set):
                logger.warning(f"tags 매개변수는 집합(set) 형태여야 합니다. 자동으로 집합으로 변환합니다: {tags}")
                try:
                    if isinstance(tags, str):
                        tags = {tags}  # 문자열이면 단일 요소 집합으로 변환
                    elif hasattr(tags, '__iter__'):
                        tags = set(tags)  # 반복 가능한 객체라면 집합으로 변환
                    else:
                        tags = {tags}  # 단일 객체인 경우 그것을 포함하는 집합 생성
                except Exception as e:
                    logger.error(f"tags 변환 오류: {e}")
                    tags = set()  # 변환 실패 시 빈 집합으로 설정
            
            # 대소문자 구분 경고
            registered_signals = set(self._callbacks.keys())
            for existing_signal in registered_signals:
                if existing_signal.lower() == signal_name.lower() and existing_signal != signal_name:
                    logger.warning(f"대소문자가 다른 유사한 시그널이 이미 등록되어 있습니다: '{existing_signal}' vs '{signal_name}'")
                    logger.warning("시그널 이름은 대소문자를 구분합니다. 정확한 이름을 사용하세요.")
            
            # 이미 등록된 콜백인지 확인
            existing_callbacks = self._callbacks.get(signal_name, [])
            for existing_callback in existing_callbacks:
                if (existing_callback.callback == callback and 
                    existing_callback.sender == sender and 
                    existing_callback.filter_condition == filter_condition):
                    logger.warning(f"콜백이 이미 등록되어 있습니다: {signal_name} - {callback.__name__}")
                    return

            # is_async를 명시적으로 받도록
            if is_async is None:
                is_async = asyncio.iscoroutinefunction(callback)
            callback_obj = SignalCallback(
                callback=callback,
                sender=sender,
                priority=priority,
                is_async=is_async,
                filter_condition=filter_condition,
                tags=tags or set(),
                group=group,
                channel=channel,
                stop_propagation=stop_propagation
            )
            
            # 콜백 등록
            self._callbacks[signal_name].append(callback_obj)
            callback_index = len(self._callbacks[signal_name]) - 1
            
            # 인덱스 업데이트
            for tag in callback_obj.tags:
                self._update_index(self._tag_index, tag, signal_name, callback_index)
            if group:
                self._update_index(self._group_index, group, signal_name, callback_index)
            if channel:
                self._update_index(self._channel_index, channel, signal_name, callback_index)
            
            self._callbacks[signal_name].sort(key=lambda x: x.priority.value, reverse=True)
            self._stats.active_callbacks += 1
            logger.info(f"콜백 등록 완료: {signal_name} - {callback.__name__}")

    def unregister_callback(self, signal_name: str, callback: Callable, sender: Any = None):
        """콜백 제거 (스레드 안전)"""
        with self._lock:
            if signal_name in self._callbacks:
                original_count = len(self._callbacks[signal_name])
                removed_indices = set()
                
                # 제거할 콜백 찾기
                for i, cb in enumerate(self._callbacks[signal_name]):
                    if cb.callback == callback and (sender is None or cb.sender == sender):
                        removed_indices.add(i)
                
                if removed_indices:
                    # 인덱스에서 제거
                    self._remove_from_index(self._tag_index, signal_name, removed_indices)
                    self._remove_from_index(self._group_index, signal_name, removed_indices)
                    self._remove_from_index(self._channel_index, signal_name, removed_indices)
                    
                    # 콜백 제거
                    self._callbacks[signal_name] = [
                        cb for i, cb in enumerate(self._callbacks[signal_name])
                        if i not in removed_indices
                    ]
                    
                    # 빈 리스트 제거
                    if not self._callbacks[signal_name]:
                        del self._callbacks[signal_name]
                    
                    removed_count = original_count - len(self._callbacks.get(signal_name, []))
                    self._stats.active_callbacks -= removed_count
                    if removed_count > 0:
                        logger.info(f"콜백 제거 완료: {signal_name} - {callback.__name__} ({removed_count}개)")

    def get_callbacks_by_tag(self, tag: str) -> List[Tuple[str, SignalCallback]]:
        """태그로 콜백을 검색합니다."""
        with self._lock:
            return [
                (signal_name, self._callbacks[signal_name][idx])
                for signal_name, idx in self._tag_index.get(tag, set())
            ]

    def get_callbacks_by_group(self, group: str) -> List[Tuple[str, SignalCallback]]:
        """그룹으로 콜백을 검색합니다."""
        with self._lock:
            return [
                (signal_name, self._callbacks[signal_name][idx])
                for signal_name, idx in self._group_index.get(group, set())
            ]

    def get_callbacks_by_channel(self, channel: str) -> List[Tuple[str, SignalCallback]]:
        """채널로 콜백을 검색합니다."""
        with self._lock:
            return [
                (signal_name, self._callbacks[signal_name][idx])
                for signal_name, idx in self._channel_index.get(channel, set())
            ]

    def send_signal(
        self,
        signal_name: str,
        data: Any = None,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL,
        tags: Set[str] = None,
        group: Optional[str] = None,
        channel: Optional[str] = None
    ):
        """시그널을 전송합니다."""
        if not self._running:
            raise RuntimeError("시그널 매니저가 종료되었습니다.")
        
        # 대소문자 구분 경고 추가
        with self._lock:
            registered_signals = set(self._callbacks.keys())
            found_similar = False
            for existing_signal in registered_signals:
                if existing_signal.lower() == signal_name.lower() and existing_signal != signal_name:
                    logger.warning(f"대소문자가 다른 유사한 시그널을 발견했습니다: '{existing_signal}' vs '{signal_name}'")
                    logger.warning("시그널 이름은 대소문자를 구분합니다. 정확한 이름을 사용하세요.")
                    found_similar = True
            
            if signal_name not in registered_signals:
                if found_similar:
                    logger.warning(f"시그널 '{signal_name}'에 대한 콜백이 없지만 유사한 이름이 있습니다.")
                else:
                    logger.warning(f"시그널 '{signal_name}'에 대한 콜백이 없습니다.")
            
        # 우선순위 값을 정수로 변환
        priority_value = {
            SignalPriority.LOW: 3,
            SignalPriority.NORMAL: 2,
            SignalPriority.HIGH: 1,
            SignalPriority.CRITICAL: 0
        }[priority]
        
        # 태그 타입 검증 추가
        if tags is not None and not isinstance(tags, set):
            logger.warning(f"tags 매개변수는 집합(set) 형태여야 합니다. 자동으로 집합으로 변환합니다: {tags}")
            try:
                if isinstance(tags, str):
                    tags = {tags}  # 문자열이면 단일 요소 집합으로 변환
                elif hasattr(tags, '__iter__'):
                    tags = set(tags)  # 반복 가능한 객체라면 집합으로 변환
                else:
                    tags = {tags}  # 단일 객체인 경우 그것을 포함하는 집합 생성
            except Exception as e:
                logger.error(f"tags 변환 오류: {e}")
                tags = set()  # 변환 실패 시 빈 집합으로 설정
        
        # 시그널 데이터를 큐에 추가
        signal_data = (signal_name, data, sender, tags or set(), group, channel)
        self._signal_queue.put((priority_value, signal_data))
        
        logger.debug(f"시그널 전송: {signal_name} (우선순위: {priority.name})")

    def get_signal_stats(self) -> SignalStats:
        return self._stats

    def reset_signal_stats(self):
        with self._lock:
            self._stats = SignalStats()

    def shutdown(self):
        """시그널 매니저 종료"""
        self._running = False
        # shutdown 호출 여부 표시
        self._shutdown_called = True
        # 무한 대기 시그널 목록 비우기
        self._infinite_wait_signals.clear()
        
        if self._processing_thread.is_alive():
            self._processing_thread.join(timeout=5)
        self._executor.shutdown(wait=True)
        if self._event_loop and self._event_loop.is_running():
            self._event_loop.call_soon_threadsafe(self._event_loop.stop)
            self._event_loop_thread.join(timeout=5)
            self._event_loop.close()
        
        logger.info("시그널 매니저가 정상적으로 종료되었습니다.")

    def on(
        self,
        signal_name: str,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL,
        filter_condition: Optional[Callable] = None,
        tags: Set[str] = None,
        group: Optional[str] = None,
        channel: Optional[str] = None,
        stop_propagation: bool = False
    ):
        """
        시그널 핸들러를 등록하기 위한 데코레이터입니다.
        
        Args:
            signal_name (str): 시그널 이름
            sender (Any, optional): 시그널 발신자
            priority (SignalPriority, optional): 시그널 우선순위
            filter_condition (Callable, optional): 시그널 필터링 조건
            tags (Set[str], optional): 시그널 태그
            group (str, optional): 시그널 그룹
            channel (str, optional): 시그널 채널
            stop_propagation (bool, optional): 시그널 전파 중단 여부
        """
        def decorator(func: Callable):
            is_async = asyncio.iscoroutinefunction(func)
            if is_async:
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                wrapped_func = async_wrapper
            else:
                wrapped_func = func

            self.register_callback(
                signal_name=signal_name,
                callback=wrapped_func,
                sender=sender,
                priority=priority,
                filter_condition=filter_condition,
                tags=tags,
                group=group,
                channel=channel,
                stop_propagation=stop_propagation,
                is_async=is_async
            )
            return wrapped_func
        return decorator

    def on_tag(
        self,
        tag: str,
        signal_name: str = None,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL,
        filter_condition: Optional[Callable] = None,
        group: Optional[str] = None,
        channel: Optional[str] = None,
        stop_propagation: bool = False
    ):
        """
        특정 태그를 가진 시그널 핸들러를 등록하기 위한 데코레이터입니다.
        
        Args:
            tag (str): 시그널 태그
            signal_name (str, optional): 시그널 이름
            sender (Any, optional): 시그널 발신자
            priority (SignalPriority, optional): 시그널 우선순위
            filter_condition (Callable, optional): 시그널 필터링 조건
            group (str, optional): 시그널 그룹
            channel (str, optional): 시그널 채널
            stop_propagation (bool, optional): 시그널 전파 중단 여부
        """
        def decorator(func: Callable):
            is_async = asyncio.iscoroutinefunction(func)
            if is_async:
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                wrapped_func = async_wrapper
            else:
                wrapped_func = func

            self.register_callback(
                signal_name=signal_name or func.__name__,
                callback=wrapped_func,
                sender=sender,
                priority=priority,
                filter_condition=filter_condition,
                tags={tag},
                group=group,
                channel=channel,
                stop_propagation=stop_propagation,
                is_async=is_async
            )
            return wrapped_func
        return decorator

    def on_group(
        self,
        group: str,
        signal_name: str = None,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL,
        filter_condition: Optional[Callable] = None,
        tags: Set[str] = None,
        channel: Optional[str] = None,
        stop_propagation: bool = False
    ):
        """
        특정 그룹의 시그널 핸들러를 등록하기 위한 데코레이터입니다.
        
        Args:
            group (str): 시그널 그룹
            signal_name (str, optional): 시그널 이름
            sender (Any, optional): 시그널 발신자
            priority (SignalPriority, optional): 시그널 우선순위
            filter_condition (Callable, optional): 시그널 필터링 조건
            tags (Set[str], optional): 시그널 태그
            channel (str, optional): 시그널 채널
            stop_propagation (bool, optional): 시그널 전파 중단 여부
        """
        def decorator(func: Callable):
            is_async = asyncio.iscoroutinefunction(func)
            if is_async:
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                wrapped_func = async_wrapper
            else:
                wrapped_func = func

            self.register_callback(
                signal_name=signal_name or func.__name__,
                callback=wrapped_func,
                sender=sender,
                priority=priority,
                filter_condition=filter_condition,
                tags=tags,
                group=group,
                channel=channel,
                stop_propagation=stop_propagation,
                is_async=is_async
            )
            return wrapped_func
        return decorator

    def receive_signal(self, signal_name: str, timeout: Optional[float] = None) -> Any:
        """
        시그널을 수신합니다. 
        이 함수는 시그널이 도착할 때까지 대기하지만, 메인 스레드를 차단하지 않습니다.
        
        Args:
            signal_name (str): 수신할 시그널 이름
            timeout (Optional[float]): 타임아웃 시간(초). None이면 무기한 대기합니다.
                                       프로그램 종료 시 shutdown() 호출 필요.
        """
        # 무한 대기일 경우 shutdown 경고 추가
        if timeout is None:
            # 프로그램에 shutdown() 호출이 있는지 소스 코드에서 확인 시도
            has_shutdown_call = False
            try:
                # 호출 스택의 모든 프레임 검사
                for frame_info in inspect.stack():
                    with open(frame_info.filename, 'r') as f:
                        content = f.read()
                        if "shutdown()" in content or "shutdown" in content:
                            has_shutdown_call = True
                            break
            except Exception:
                pass  # 파일 접근 오류 등은 무시

            if not has_shutdown_call:
                logger.warning("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                logger.warning(f"시그널 '{signal_name}'을 무기한 대기합니다. 메모리 누수 방지를 위해 프로그램 종료 전 반드시 signal_manager.shutdown()을 호출하세요!")
                logger.warning("shutdown() 호출이 코드에서 감지되지 않았습니다. 이로 인해 프로그램이 종료되지 않을 수 있습니다.")
                logger.warning("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"[경고] 시그널 '{signal_name}'을 무기한 대기합니다. 프로그램 종료 전 반드시 signal_manager.shutdown()을 호출하세요!", file=sys.stderr)
            
            # 무한 대기 시그널 목록에 추가
            self._infinite_wait_signals.add(signal_name)
        
        # 대소문자 구분 경고 추가
        with self._lock:
            registered_signals = set(self._callbacks.keys())
            found_similar = False
            for existing_signal in registered_signals:
                if existing_signal.lower() == signal_name.lower() and existing_signal != signal_name:
                    logger.warning(f"대소문자가 다른 유사한 시그널을 발견했습니다: '{existing_signal}' vs '{signal_name}'")
                    logger.warning("시그널 이름은 대소문자를 구분합니다. 정확한 이름을 사용하세요.")
                    found_similar = True
        
        # 이벤트 객체 생성
        event = threading.Event()
        result = [None]
        
        def signal_handler(signal_name, data, sender):
            result[0] = data
            event.set()  # 이벤트 설정하여 대기 중인 스레드 깨우기
            # 시그널을 수신했으면 무한 대기 목록에서 제거
            if timeout is None:
                self._infinite_wait_signals.discard(signal_name)
        
        # 콜백 등록
        self.register_callback(signal_name, signal_handler)
        
        # 작은 시간 지연으로 시그널 처리 기회 제공
        time.sleep(0.1)
        
        # 메인 스레드가 계속 실행되도록 non-daemon 스레드 사용
        def wait_for_signal():
            if timeout is not None:
                # 타임아웃이 지정된 경우
                event.wait(timeout)
            else:
                # 타임아웃이 None인 경우 무기한 대기
                logger.info(f"시그널 '{signal_name}'을 무기한 대기합니다. 종료 시 shutdown() 호출 필수.")
                event.wait()
            
            # 결과 확인 및 출력
            if result[0] is not None:
                print(f"수신된 시그널 데이터: {result[0]}")
                # 시그널을 수신했으면 무한 대기 목록에서 제거
                if timeout is None:
                    self._infinite_wait_signals.discard(signal_name)
            else:
                if timeout is not None:
                    print(f"시그널이 {timeout}초 내에 수신되지 않았습니다.")
                else:
                    print("시그널 수신이 중단되었습니다.")
                    # 중단되었으면 무한 대기 목록에서 제거
                    self._infinite_wait_signals.discard(signal_name)
                
                # 결과가 없는 경우 대소문자 검사 다시 진행
                with self._lock:
                    if found_similar:
                        print("대소문자 불일치 문제가 있을 수 있습니다. 로그를 확인하세요.")
            
            # 콜백 정리 (중요)
            self.unregister_callback(signal_name, signal_handler)
        
        # non-daemon 스레드로 생성하여 메인 프로그램이 종료되어도 실행 보장
        t = threading.Thread(target=wait_for_signal, daemon=False)
        t.start()
        
        return result[0]  # 아직 값이 없으면 None 반환

    def monitor_signal(self, signal_name: str, callback: Callable[[Any], None], timeout: Optional[float] = None):
        """
        지속적으로 시그널을 모니터링합니다.
        
        Args:
            signal_name (str): 모니터링할 시그널 이름
            callback (Callable[[Any], None]): 시그널 수신시 호출될 콜백 함수
            timeout (Optional[float]): 타임아웃 시간 (초)
        """
        signal_queue = queue.Queue()
        stop_event = threading.Event()
        
        def signal_handler(signal_name, data, sender):
            signal_queue.put(data)
            
        # 콜백 등록
        self.register_callback(signal_name, signal_handler)
        
        def monitor_loop():
            start_time = time.time()
            while not stop_event.is_set():
                try:
                    # 시그널 대기
                    data = signal_queue.get(timeout=0.1)  # 0.1초마다 체크
                    callback(data)
                    
                    # 타임아웃 체크
                    if timeout and (time.time() - start_time) > timeout:
                        break
                        
                except queue.Empty:
                    continue
                    
            # 모니터링 종료시 콜백 제거
            self.unregister_callback(signal_name, signal_handler)
        
        # 모니터링 스레드 시작
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        return stop_event  # stop_event를 반환하여 외부에서 모니터링 중단 가능

    async def monitor_signal_async(self, signal_name: str, callback: Callable[[Any], None], timeout: Optional[float] = None):
        """
        비동기 방식으로 지속적으로 시그널을 모니터링합니다.
        
        Args:
            signal_name (str): 모니터링할 시그널 이름
            callback (Callable[[Any], None]): 시그널 수신시 호출될 콜백 함수
            timeout (Optional[float]): 타임아웃 시간 (초)
        """
        signal_queue = asyncio.Queue()
        stop_event = asyncio.Event()
        
        def signal_handler(signal_name, data, sender):
            asyncio.run_coroutine_threadsafe(signal_queue.put(data), self._event_loop)
            
        # 콜백 등록
        self.register_callback(signal_name, signal_handler)
        
        async def monitor_loop():
            start_time = time.time()
            while not stop_event.is_set():
                try:
                    # 시그널 대기
                    data = await asyncio.wait_for(signal_queue.get(), timeout=0.1)  # 0.1초마다 체크
                    callback(data)
                    
                    # 타임아웃 체크
                    if timeout and (time.time() - start_time) > timeout:
                        break
                        
                except asyncio.TimeoutError:
                    continue
                    
            # 모니터링 종료시 콜백 제거
            self.unregister_callback(signal_name, signal_handler)
        
        # 모니터링 태스크 시작
        monitor_task = asyncio.create_task(monitor_loop())
        
        return stop_event  # stop_event를 반환하여 외부에서 모니터링 중단 가능

    async def receive_signal_async(self, signal_name: str, timeout: Optional[float] = None) -> Any:
        """
        비동기 방식으로 시그널을 수신합니다.
        """
        future = asyncio.Future()
        
        def signal_handler(signal_name, data, sender):
            if not future.done():
                future.set_result(data)
            
        # 임시 콜백 등록
        self.register_callback(signal_name, signal_handler)
        
        try:
            # 시그널 대기
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"시그널 수신 타임아웃: {signal_name}")
        finally:
            # 임시 콜백 제거
            self.unregister_callback(signal_name, signal_handler)

# 싱글톤 인스턴스 생성
signal_manager = SignalManager()