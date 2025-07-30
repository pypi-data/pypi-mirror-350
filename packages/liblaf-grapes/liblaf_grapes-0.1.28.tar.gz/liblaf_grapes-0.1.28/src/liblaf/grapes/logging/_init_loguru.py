import functools
import logging
import sys
import types
from collections.abc import Sequence
from typing import Unpack

import loguru
from environs import env
from loguru import logger

from ._intercept import setup_loguru_logging_intercept
from ._level import DEFAULT_LEVELS, add_level
from ._std import clear_handlers
from .handler import file_handler, jsonl_handler, rich_handler


def init_loguru(
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
    *,
    enable_link: bool = True,
    **kwargs: Unpack["loguru.BasicHandlerConfig"],
) -> None:
    traceback_install()
    if handlers is None:
        handlers: list[loguru.HandlerConfig] = [
            rich_handler(enable_link=enable_link, **kwargs)
        ]
        if env.path("LOGGING_FILE", default=None):
            handlers.append(file_handler(**kwargs))  # pyright: ignore[reportArgumentType]
        if env.path("LOGGING_JSONL", default=None):
            handlers.append(jsonl_handler(**kwargs))  # pyright: ignore[reportArgumentType]
    logger.configure(handlers=handlers)
    for lvl in levels or DEFAULT_LEVELS:
        add_level(**lvl)
    setup_loguru_logging_intercept(kwargs.get("level", logging.NOTSET))
    clear_handlers()


def traceback_install(level: int | str = "CRITICAL", message: str = "") -> None:
    sys.excepthook = functools.partial(excepthook, level=level, message=message)


def excepthook(
    exc_type: type[BaseException],
    exc_value: BaseException,
    traceback: types.TracebackType,
    *,
    level: int | str = "CRITICAL",
    message: str = "",
) -> None:
    logger.opt(exception=(exc_type, exc_value, traceback)).log(level, message)
