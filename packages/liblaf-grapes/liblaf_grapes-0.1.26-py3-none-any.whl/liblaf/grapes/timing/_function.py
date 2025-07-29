import functools
from collections.abc import Callable

from liblaf.grapes import pretty

from . import callback
from ._base import TimerRecords


class TimedFunction[**P, T]:
    timing: TimerRecords
    _fn: Callable[P, T]

    def __init__(self, fn: Callable[P, T], /, *, timing: TimerRecords) -> None:
        self._fn = fn
        self.timing = timing.replace_if_none(
            name=pretty.func(fn).plain or "Function",
            cb_finish=callback.log_summary(depth=3),
            cb_stop=callback.log_record(depth=4),
        )
        functools.update_wrapper(self, fn)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        self.timing.start()
        result: T = self._fn(*args, **kwargs)
        self.timing.stop()
        return result
