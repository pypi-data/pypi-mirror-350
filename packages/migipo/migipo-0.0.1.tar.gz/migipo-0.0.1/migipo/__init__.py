from __future__ import annotations

import sys
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsWrite


_verbose = False


def set_verbose(val: bool) -> None:
    global _verbose
    _verbose = val


class LogType(Enum):
    DEBUG = 0
    INFO = 1
    ERROR = 2


def log(msg: str, file: SupportsWrite[str] | None = sys.stderr, log_type: LogType = LogType.DEBUG) -> None:
    if _verbose or log_type == LogType.ERROR:
        print(f'[ migipo ] [ {log_type.name} ] {msg}', file=file)
