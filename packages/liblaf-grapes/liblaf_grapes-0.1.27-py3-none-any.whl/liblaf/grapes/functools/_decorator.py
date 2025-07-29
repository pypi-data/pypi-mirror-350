import functools
from collections.abc import Callable

from liblaf.grapes.typed import (
    Decorator,
    DecoratorWithArguments,
    DecoratorWithOptionalArguments,
)


def decorator_with_optional_arguments[**Q](
    caller: DecoratorWithArguments[Q],
) -> DecoratorWithOptionalArguments[Q]:
    @functools.wraps(caller)
    def wrapper[**P, T](
        func: Callable[P, T] | None = None, /, *args, **kwargs
    ) -> Callable[P, T] | Decorator:
        if func is None:
            return caller(*args, **kwargs)
        return caller(*args, **kwargs)(func)

    return wrapper  # pyright: ignore[reportReturnType]
