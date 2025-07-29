import functools
from collections.abc import Sequence
from typing import overload

from ._base import Callback, TimerRecords


@overload
def log_record(
    *,
    depth: int = 1,
    index: int = -1,
    level: int | str = "DEBUG",
) -> Callback: ...
@overload
def log_record(
    records: TimerRecords,
    /,
    *,
    depth: int = 1,
    index: int = -1,
    level: int | str = "DEBUG",
) -> None: ...
def log_record(
    records: TimerRecords | None = None,
    /,
    *,
    depth: int = 1,
    index: int = -1,
    level: int | str = "DEBUG",
) -> Callback | None:
    if records is None:
        return functools.partial(log_record, depth=depth, index=index, level=level)  # pyright: ignore[reportReturnType]
    records.log_record(depth=depth, index=index, level=level)
    return None


@overload
def log_summary(
    *,
    depth: int = 1,
    level: int | str = "INFO",
    stats: Sequence[str] = ("mean+std", "median"),
) -> Callback: ...
@overload
def log_summary(
    records: TimerRecords,
    /,
    *,
    depth: int = 1,
    level: int | str = "INFO",
    stats: Sequence[str] = ("mean+std", "median"),
) -> None: ...
def log_summary(
    records: TimerRecords | None = None,
    /,
    *,
    depth: int = 1,
    level: int | str = "INFO",
    stats: Sequence[str] = ("mean+std", "median"),
) -> Callback | None:
    if records is None:
        return functools.partial(log_summary, depth=depth, level=level, stats=stats)
    records.log_summary(depth=depth, level=level, stats=stats)
    return None


__all__ = ["log_record", "log_summary"]
