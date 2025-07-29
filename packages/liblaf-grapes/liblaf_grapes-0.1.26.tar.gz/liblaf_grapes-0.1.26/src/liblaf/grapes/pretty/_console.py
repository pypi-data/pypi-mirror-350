import functools
from typing import IO, Literal

import rich
from environs import env
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from liblaf.grapes import path
from liblaf.grapes.typed import PathLike


def theme() -> Theme:
    return Theme(
        {
            "logging.level.notset": Style(dim=True),
            "logging.level.trace": Style(color="cyan", bold=True),
            "logging.level.debug": Style(color="blue", bold=True),
            "logging.level.icecream": Style(color="magenta", bold=True),
            "logging.level.info": Style(bold=True),
            "logging.level.success": Style(color="green", bold=True),
            "logging.level.warning": Style(color="yellow", bold=True),
            "logging.level.error": Style(color="red", bold=True),
            "logging.level.critical": Style(color="red", bold=True, reverse=True),
        },
        inherit=True,
    )


@functools.cache
def get_console(
    file: Literal["stdout", "stderr"] | IO | PathLike = "stdout", **kwargs
) -> Console:
    kwargs.setdefault("force_terminal", force_terminal(file))
    kwargs.setdefault("theme", theme())
    match file:
        case "stdout":
            rich.reconfigure(**kwargs)
            return rich.get_console()
        case "stderr":
            kwargs.setdefault("stderr", True)
            return Console(**kwargs)
        case IO():
            return Console(file=file, **kwargs)
        case file:
            kwargs.setdefault("width", 128)
            return Console(file=path.as_path(file).open("w"), **kwargs)


def force_terminal(file: Literal["stdout", "stderr"] | IO | PathLike) -> bool | None:
    """...

    References:
        1. <https://force-color.org/>
        2. <https://no-color.org/>
    """
    if file not in ("stdout", "stderr"):
        return None
    if env.bool("FORCE_COLOR", None):
        return True
    if env.bool("NO_COLOR", None):
        return False
    if env.bool("GITHUB_ACTIONS", None):
        return True
    return None
