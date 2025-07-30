"""
fnsignal - Python 시그널 처리 라이브러리
"""

__version__ = "2.5.0"

from .fnsignal import (
    SignalManager,
    SignalPriority,
    SignalCallback,
    SignalStats,
    signal_manager,
    setup_logging
)

__all__ = [
    "SignalManager",
    "SignalPriority",
    "SignalCallback",
    "SignalStats",
    "signal_manager",
    "setup_logging"
]

# 패키지 레벨에 함수들을 직접 할당
globals().update({
    "signal_manager": signal_manager,
    "SignalPriority": SignalPriority,
    "SignalCallback": SignalCallback,
    "SignalStats": SignalStats,
    "setup_logging": setup_logging
}) 