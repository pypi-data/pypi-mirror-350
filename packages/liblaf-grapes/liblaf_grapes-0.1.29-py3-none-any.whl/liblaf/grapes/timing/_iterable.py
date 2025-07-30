from collections.abc import Iterable, Iterator

from . import callback
from ._base import TimerRecords


class TimedIterable[T]:
    timing: TimerRecords
    _iterable: Iterable[T]
    _total: int | None = None

    def __init__(
        self,
        iterable: Iterable[T],
        /,
        *,
        timing: TimerRecords,
        total: int | None = None,
    ) -> None:
        self.timing = timing.replace_if_none(
            name="Iterable",
            cb_stop=callback.log_record(depth=4),
            cb_finish=callback.log_summary(depth=4),
        )
        self._iterable = iterable
        self._total = total

    def __contains__(self, x: object, /) -> bool:
        return x in self._iterable  # pyright: ignore[reportOperatorIssue]

    def __len__(self) -> int:
        if self._total is None:
            return len(self._iterable)  # pyright: ignore[reportArgumentType]
        return self._total

    def __iter__(self) -> Iterator[T]:
        # measure generator + consumer time
        self.timing.start()
        for item in self._iterable:
            yield item
            self.timing.stop()
            self.timing.start()
        self.timing.finish()
