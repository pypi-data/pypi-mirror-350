import contextlib
import enum
import types
from collections.abc import Callable, Iterable, Sequence
from typing import Self, overload, override

import attrs

from liblaf.grapes import utils
from liblaf.grapes.timing import callback

from ._base import Callback, TimerRecords
from ._function import TimedFunction
from ._iterable import TimedIterable


class TimerMode(enum.Enum):
    CONTEXT_MANAGER = enum.auto()
    MANUAL = enum.auto()


@attrs.define
class Timer(
    contextlib.AbstractAsyncContextManager,
    contextlib.AbstractContextManager,
    TimerRecords,
):
    _mode: TimerMode = TimerMode.MANUAL
    _user_name: str | None = attrs.field(default=None, init=False)
    _user_timers: Sequence[str] | None = attrs.field(default=None, init=False)
    _user_cb_finish: Callback | None = attrs.field(default=None, init=False)
    _user_cb_start: Callback | None = attrs.field(default=None, init=False)
    _user_cb_stop: Callback | None = attrs.field(default=None, init=False)

    async def __aenter__(self) -> Self:
        self.mode = TimerMode.CONTEXT_MANAGER
        super().start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        super().stop()

    @overload
    def __call__[**P, T](self, fn: Callable[P, T], /) -> TimedFunction[P, T]: ...
    @overload
    def __call__[**P, T](
        self, iterable: Iterable[T], /, *, total: int | None = None
    ) -> TimedIterable[T]: ...
    def __call__[**P, T](
        self,
        fn_or_iterable: Callable[P, T] | Iterable[T],
        /,
        *,
        total: int | None = None,
    ) -> TimedFunction[P, T] | TimedIterable[T]:
        timing = TimerRecords(
            name=self._user_name,
            timers=self.timers,
            cb_finish=self._user_cb_finish,
            cb_start=self._user_cb_start,
            cb_stop=self._user_cb_stop,
        )
        if callable(fn_or_iterable):
            return TimedFunction(fn_or_iterable, timing=timing)
        return TimedIterable(fn_or_iterable, timing=timing, total=total)

    def __enter__(self) -> Self:
        self.mode = TimerMode.CONTEXT_MANAGER
        super().start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        super().stop()

    def __attrs_post_init__(self) -> None:
        self._user_name = self.name
        self._user_cb_finish = self.cb_finish
        self._user_cb_start = self.cb_start
        self._user_cb_stop = self.cb_stop

    @property
    def mode(self) -> TimerMode:
        return self._mode

    @mode.setter
    def mode(self, value: TimerMode) -> None:
        if self._mode == value:
            return
        match value:
            case TimerMode.CONTEXT_MANAGER:
                self.name = self._user_name or "Block"
                self.cb_stop = self._user_cb_stop or callback.log_record(depth=4)
                self.cb_finish = self._user_cb_finish or callback.log_summary(depth=3)
            case TimerMode.MANUAL:
                self.name = self._user_name or "Timer"
                self.cb_stop = self._user_cb_stop or callback.log_record(depth=3)
                self.cb_finish = self._user_cb_finish or callback.log_summary(depth=3)
        self._mode = value

    @override
    def replace_if_none(
        self,
        *,
        name: str | None = None,
        timers: Sequence[str] | None = None,
        cb_finish: Callback | None = None,
        cb_start: Callback | None = None,
        cb_stop: Callback | None = None,
    ) -> Self:
        return attrs.evolve(
            self,
            name=utils.first_not_none(self._user_name, name),
            timers=utils.first_not_none(self._user_timers, timers),
            cb_finish=utils.first_not_none(self._user_cb_finish, cb_finish),
            cb_start=utils.first_not_none(self._user_cb_start, cb_start),
            cb_stop=utils.first_not_none(self._user_cb_stop, cb_stop),
        )

    @override
    def start(self) -> None:
        self.mode = TimerMode.MANUAL
        super().start()


@overload
def timer[**P, T](
    name: str | None = None,
    *,
    timers: Sequence[str] = ("perf",),
    cb_finish: Callback | None = None,
    cb_start: Callback | None = None,
    cb_stop: Callback | None = None,
) -> Timer: ...
@overload
def timer[**P, T](
    fn: Callable[P, T],
    /,
    *,
    name: str | None = None,
    timers: Sequence[str] = ("perf",),
    cb_finish: Callback | None = None,
    cb_start: Callback | None = None,
    cb_stop: Callback | None = None,
) -> TimedFunction[P, T]: ...
@overload
def timer[**P, T](
    iterable: Iterable[T],
    /,
    *,
    name: str | None = None,
    timers: Sequence[str] = ("perf",),
    total: int | None = None,
    cb_finish: Callback | None = None,
    cb_start: Callback | None = None,
    cb_stop: Callback | None = None,
) -> TimedIterable[T]: ...
def timer(*args, **kwargs) -> TimedFunction | TimedIterable | Timer:
    fn_iterable_name: Callable | Iterable | str | None = args[0] if args else None
    if callable(fn_iterable_name):
        return TimedFunction(fn_iterable_name, timing=TimerRecords(**kwargs))
    if isinstance(fn_iterable_name, str):
        kwargs.setdefault("name", fn_iterable_name)
        return Timer(**kwargs)
    if isinstance(fn_iterable_name, Iterable):
        total: int | None = kwargs.pop("total", None)
        return TimedIterable(
            fn_iterable_name, timing=TimerRecords(**kwargs), total=total
        )
    return Timer(**kwargs)
