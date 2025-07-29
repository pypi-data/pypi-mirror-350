import functools
from typing import Any

from loguru import logger
from typing_extensions import deprecated

# https://stackoverflow.com/a/66062313


@deprecated("Use `filter_once()` + `logger.bind(once=True).trace(...)` instead.")
@functools.lru_cache
def trace_once(message: Any, *args, **kwargs) -> None:
    logger.trace(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).debug(...)` instead.")
@functools.lru_cache
def debug_once(message: Any, *args, **kwargs) -> None:
    logger.debug(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).info(...)` instead.")
@functools.lru_cache
def info_once(message: Any, *args, **kwargs) -> None:
    logger.info(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).success(...)` instead.")
@functools.lru_cache
def success_once(message: Any, *args, **kwargs) -> None:
    logger.success(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).warning(...)` instead.")
@functools.lru_cache
def warning_once(message: Any, *args, **kwargs) -> None:
    logger.warning(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).error(...)` instead.")
@functools.lru_cache
def error_once(message: Any, *args, **kwargs) -> None:
    logger.error(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).critical(...)` instead.")
@functools.lru_cache
def critical_once(message: Any, *args, **kwargs) -> None:
    logger.critical(message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).log(...)` instead.")
@functools.lru_cache
def log_once(level: int | str, message: Any, *args, **kwargs) -> None:
    logger.log(level, message, *args, **kwargs)


@deprecated("Use `filter_once()` + `logger.bind(once=True).exception(...)` instead.")
@functools.lru_cache
def exception_once(message: Any, *args, **kwargs) -> None:
    logger.exception(message, *args, **kwargs)
