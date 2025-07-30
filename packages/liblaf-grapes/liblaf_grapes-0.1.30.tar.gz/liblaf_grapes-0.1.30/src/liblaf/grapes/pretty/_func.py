import inspect
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Literal

import autoregistry
from rich.style import Style
from rich.text import Text

_func = autoregistry.Registry(prefix="_func_")


def func(obj: Callable, *, style: Literal["short", "long"] = "short") -> Text:
    return _func[style](obj)


@_func
def _func_short(obj: Callable) -> Text:
    obj = inspect.unwrap(obj)
    text = Text()
    name: str = _get_name(obj)
    source_file: Path | None = _get_source_file(obj)
    lineno: int = _get_source_lineno(obj)
    if source_file and lineno:
        text.append(
            f"{name}()",
            style=Style(link=f"{source_file.as_uri()}#{lineno}"),
        )
    else:
        text.append(f"{name}()")
    return text


@_func
def _func_long(obj: Callable) -> Text:
    obj = inspect.unwrap(obj)
    text = Text()
    module: str = _get_module(obj)
    qualname: str = _get_qualname(obj)
    source_file: Path | None = _get_source_file(obj)
    lineno: int = _get_source_lineno(obj)
    if source_file:
        text.append(module, style=Style(link=source_file.as_uri()))
        text.append(".")
        text.append(
            f"{qualname}(...)",
            style=Style(link=f"{source_file.as_uri()}#{lineno}"),
        )
    else:
        text.append(f"{module}.{qualname}(...)")
    return text


_pretty_func = func


def call(func: Callable, args: tuple, kwargs: Mapping) -> Text:  # noqa: ARG001
    # TODO: add `args` and `kwargs`
    return _pretty_func(func)


def _get_module(obj: Any) -> str:
    return getattr(obj, "__module__", "unknown")


def _get_name(obj: Any) -> str:
    return getattr(obj, "__name__", "<unknown>")


def _get_qualname(obj: Any) -> str:
    return getattr(obj, "__qualname__", "<unknown>")


def _get_source_file(obj: Any) -> Path | None:
    try:
        if source_file := inspect.getsourcefile(obj):
            return Path(source_file)
    except TypeError:
        pass
    return None


def _get_source_lineno(obj: Any) -> int:
    try:
        lineno: int
        _lines, lineno = inspect.getsourcelines(obj)
    except (OSError, TypeError):
        pass
    else:
        return lineno
    return 0
