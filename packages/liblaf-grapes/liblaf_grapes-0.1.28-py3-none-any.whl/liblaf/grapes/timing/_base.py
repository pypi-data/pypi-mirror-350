import collections
import math
import statistics
import textwrap
from collections.abc import Callable, Generator, Mapping, Sequence
from typing import Self, overload, override

import attrs
from loguru import logger

from liblaf.grapes import human, utils

from ._get_time import get_time


@attrs.define
class BaseTimer:
    name: str | None = attrs.field(default=None)
    timers: Sequence[str] = attrs.field(default=("perf",))
    _time_start: dict[str, float] = attrs.field(init=False, factory=dict)
    _time_stop: dict[str, float] = attrs.field(init=False, factory=dict)

    def __bool__(self) -> bool:
        return True

    @property
    def default_timer(self) -> str:
        return self.timers[0]

    @property
    def record(self) -> Mapping[str, float]:
        return {timer: self.elapsed(timer) for timer in self.timers}

    def elapsed(self, timer: str | None = None) -> float:
        if timer is None:
            timer = self.default_timer
        if timer in self._time_stop:
            return self._time_stop[timer] - self._time_start[timer]
        return get_time(timer) - self._time_start[timer]

    def start(self) -> None:
        for timer in self.timers:
            self._time_start[timer] = get_time(timer)
        self._time_stop.clear()

    def stop(self) -> None:
        for timer in self.timers:
            self._time_stop[timer] = get_time(timer)


type Callback = Callable[["TimerRecords"], None]


@attrs.define
class TimerRecords(BaseTimer):
    cb_finish: Callable | None = attrs.field(default=None)
    cb_start: Callable | None = attrs.field(default=None)
    cb_stop: Callable | None = attrs.field(default=None)
    _records: dict[str, list[float]] = attrs.field(
        init=False, factory=lambda: collections.defaultdict(list)
    )

    @overload
    def __getitem__(self, key: int) -> Mapping[str, float]: ...
    @overload
    def __getitem__(self, key: str) -> Sequence[float]: ...
    def __getitem__(self, key: int | str) -> Mapping[str, float] | Sequence[float]:
        if isinstance(key, int):
            return self.row(key)
        if isinstance(key, str):
            return self.column(key)
        raise KeyError(key)

    def __len__(self) -> int:
        return len(self._records[self.default_timer])

    @property
    def columns(self) -> Sequence[str]:
        return self.timers

    @property
    def count(self) -> int:
        return self.n_rows

    @property
    def n_columns(self) -> int:
        return len(self.timers)

    @property
    def n_rows(self) -> int:
        return len(self.column())

    def clear(self) -> None:
        self._records.clear()

    def column(self, timer: str | None = None) -> Sequence[float]:
        timer = timer or self.default_timer
        return self._records[timer]

    def human_record(self, index: int = -1) -> str:
        name: str = self.name or "Timer"
        text: str = f"{name} > "
        items: list[str] = []
        for timer, value in self[index].items():
            human_duration: str = human.human_duration(value)
            items.append(f"{timer}: {human_duration}")
        text += ", ".join(items)
        return text

    def human_summary(self, stats: Sequence[str] = ("mean+std", "median")) -> str:
        name: str = self.name or "Timer"
        header: str = f"{name} (total: {self.n_rows})"
        if self.n_rows == 0:
            return header
        body: str = ""
        for timer in self.columns:
            body += f"{timer} > "
            items: list[str] = []
            for stat in stats:
                human_stat_name: str = stat
                human_duration: str
                match stat:
                    case "max":
                        human_duration = human.human_duration(self.max(timer))
                    case "mean":
                        human_duration = human.human_duration(self.mean(timer))
                    case "mean+std":
                        human_stat_name = "mean"
                        human_duration = human.human_duration_with_variance(
                            self.mean(timer), self.std(timer)
                        )
                    case "median":
                        human_duration = human.human_duration(self.median(timer))
                    case "min":
                        human_duration = human.human_duration(self.min(timer))
                    case "std":
                        human_duration = human.human_duration(self.std(timer))
                    case _:
                        msg: str = f"Unknown statistic: {stat}"
                        raise ValueError(msg)
                items.append(f"{human_stat_name}: {human_duration}")
            body += ", ".join(items) + "\n"
        body = body.strip()
        summary: str = header + "\n" + textwrap.indent(body, "    ")
        return summary

    def iter_columns(self) -> Generator[tuple[str, Sequence[float]]]:
        yield from self._records.items()

    def iter_rows(self) -> Generator[Mapping[str, float]]:
        for index in range(self.n_rows):
            yield self.row(index)

    def log_record(
        self,
        depth: int = 1,
        index: int = -1,
        level: int | str = "DEBUG",
        threshold: float = 0.1,  # seconds
    ) -> None:
        if index == -1 and self.elapsed() < threshold:
            return
        logger.opt(depth=depth).log(level, self.human_record(index=index))

    def log_summary(
        self,
        depth: int = 1,
        level: int | str = "INFO",
        stats: Sequence[str] = ("mean+std", "median"),
    ) -> None:
        logger.opt(depth=depth).log(level, self.human_summary(stats=stats))

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
            name=utils.first_not_none(self.name, name),
            timers=utils.first_not_none(self.timers, timers),
            cb_finish=utils.first_not_none(self.cb_finish, cb_finish),
            cb_start=utils.first_not_none(self.cb_start, cb_start),
            cb_stop=utils.first_not_none(self.cb_stop, cb_stop),
        )

    def row(self, index: int) -> Mapping[str, float]:
        return {timer: values[index] for timer, values in self._records.items()}

    # region statistics

    def max(self, timer: str | None = None) -> float:
        return max(self.column(timer))

    def mean(self, timer: str | None = None) -> float:
        return statistics.mean(self.column(timer))

    def median(self, timer: str | None = None) -> float:
        return statistics.median(self.column(timer))

    def min(self, timer: str | None = None) -> float:
        return min(self.column(timer))

    def std(self, timer: str | None = None) -> float:
        column: Sequence[float] = self.column(timer)
        if len(column) < 2:
            return math.nan
        return statistics.stdev(column)

    # endregion statistics

    def _append(
        self, seconds: Mapping[str, float] = {}, nanoseconds: Mapping[str, float] = {}
    ) -> None:
        for key, value in seconds.items():
            self._records[key].append(value)
        for key, value in nanoseconds.items():
            self._records[key].append(value * 1e-9)

    @override
    def start(self) -> None:
        if callable(self.cb_start):
            self.cb_start(self)
        super().start()

    @override
    def stop(self) -> None:
        super().stop()
        self._append(seconds=self.record)
        if callable(self.cb_stop):
            self.cb_stop(self)

    def finish(self) -> None:
        if callable(self.cb_finish):
            self.cb_finish(self)
