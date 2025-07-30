import bisect
import functools
from collections.abc import Callable, Mapping
from typing import Any, Literal, NoReturn

import attrs
from rich.text import Text

from liblaf.grapes import pretty


@attrs.frozen
class Function:
    condition: Callable[..., bool]
    function: Callable
    precedence: int = 0


class NotFoundLookupError(LookupError):
    func: Callable
    args: tuple
    kwargs: Mapping

    def __init__(self, func: Callable, args: tuple, kwargs: Mapping) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"{self.pretty_call.plain} could not be resolved."

    @property
    def pretty_call(self) -> Text:
        return pretty.call(self.func, self.args, self.kwargs)


def _always_true(*args, **kwargs) -> Literal[True]:  # noqa: ARG001
    return True


def _fallback(func: Callable) -> Callable[..., NoReturn]:
    def fallback(*args, **kwargs) -> NoReturn:
        raise NotFoundLookupError(func, args, kwargs)

    return fallback


class ConditionalDispatcher:
    functions: list[Function]
    fallback: Callable

    def __init__(self) -> None:
        self.functions = []

    def __call__(self, *args, **kwargs) -> Any:
        for func in self.functions:
            try:
                if func.condition(*args, **kwargs):
                    return func.function(*args, **kwargs)
            except TypeError:
                continue
        return self.fallback(*args, **kwargs)

    def final(self, /, *, fallback: bool = False) -> Callable:
        def decorator[**P, T](func: Callable[P, T]) -> Callable[P, T]:
            if fallback:
                self.fallback = func
            else:
                self.fallback = _fallback(func)
            functools.update_wrapper(self, func)
            return self

        return decorator

    def register(
        self, condition: Callable[..., bool] = _always_true, *, precedence: int = 0
    ) -> Callable:
        def decorator[**P, T](func: Callable[P, T]) -> Callable[P, T]:
            function = Function(condition, func, precedence)
            bisect.insort(self.functions, function, key=lambda f: -f.precedence)
            return func

        return decorator
