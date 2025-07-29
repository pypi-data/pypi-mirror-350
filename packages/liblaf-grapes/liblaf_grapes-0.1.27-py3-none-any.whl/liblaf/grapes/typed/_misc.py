import os
import types
from typing import Literal

type ClassInfo = type | types.UnionType | tuple[ClassInfo, ...]
type LogLevel = (
    Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]  # noqa: PYI051
    | int
    | str
)
type PathLike = str | os.PathLike[str]
