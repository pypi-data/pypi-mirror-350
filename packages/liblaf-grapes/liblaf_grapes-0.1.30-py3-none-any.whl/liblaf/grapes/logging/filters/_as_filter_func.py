import builtins
import functools
from collections.abc import Mapping
from typing import Literal

import loguru
from loguru import _filters, logger

from liblaf.grapes.functools import ConditionalDispatcher

from .typed import Filter

dispatcher = ConditionalDispatcher()


# ref: <https://github.com/Delgan/loguru/blob/master/loguru/_logger.py#L259>


@dispatcher.register(lambda f: f is None)
def _(filter_: None) -> None:  # noqa: ARG001
    return None


@dispatcher.register(lambda f: f == "")
def _(filter_: Literal[""]) -> "loguru.FilterFunction":  # noqa: ARG001
    return _filters.filter_none


@dispatcher.register(lambda f: isinstance(f, str))
def _(filter_: str) -> "loguru.FilterFunction":
    parent: str = filter_ + "."
    length: int = len(parent)
    return functools.partial(_filters.filter_by_name, parent=parent, length=length)


@dispatcher.register(lambda f: isinstance(f, Mapping))
def _(filter_: Mapping[str, int | str]) -> "loguru.FilterFunction":
    level_per_module: dict[str, int] = {}
    for module, level_ in filter_.items():
        if module is not None and not isinstance(module, str):
            msg: str = (
                "The filter dict contains an invalid module, "
                f"it should be a string (or None), not: '{type(module).__name__}'"
            )
            raise TypeError(msg)
        if level_ is False:
            levelno_ = False
        elif level_ is True:
            levelno_ = 0
        elif isinstance(level_, str):
            try:
                levelno_: int = logger.level(level_).no
            except ValueError:
                msg = (
                    f"The filter dict contains a module '{module}' associated to a level name "
                    f"which does not exist: '{level_}'"
                )
                raise ValueError(msg) from None
        elif isinstance(level_, int):
            levelno_ = level_
        else:
            msg = (
                f"The filter dict contains a module '{module}' associated to an invalid level, "
                f"it should be an integer, a string or a boolean, not: '{type(level_).__name__}'"
            )
            raise TypeError(msg)
        if levelno_ < 0:
            msg = (
                f"The filter dict contains a module '{module}' associated to an invalid level, "
                f"it should be a positive integer, not: '{levelno_}'"
            )
            raise ValueError(msg)
        level_per_module[module] = levelno_
    return functools.partial(
        _filters.filter_by_level, level_per_module=level_per_module
    )


@dispatcher.register(lambda f: callable(f))
def _(filter_: "loguru.FilterFunction") -> "loguru.FilterFunction":
    if filter_ == builtins.filter:
        msg = (
            "The built-in 'filter()' function cannot be used as a 'filter' parameter, "
            "this is most likely a mistake (please double-check the arguments passed "
            "to 'logger.add()')."
        )
        raise ValueError(msg)
    return filter_


@dispatcher.final(fallback=True)
def as_filter_func(filter_: Filter | None) -> "loguru.FilterFunction | None":
    msg: str = f"Invalid filter, it should be a function, a string or a dict, not: '{type(filter_).__name__}'"
    raise TypeError(msg)
