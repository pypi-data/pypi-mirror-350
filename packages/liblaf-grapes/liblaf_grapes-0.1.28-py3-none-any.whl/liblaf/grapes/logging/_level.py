import contextlib
from collections.abc import Sequence

import loguru
from loguru import logger

DEFAULT_LEVELS: Sequence["loguru.LevelConfig"] = [
    {"name": "ICECREAM", "no": 15, "color": "<magenta><bold>", "icon": "🍦"}
]


def add_level(
    name: str, no: int, color: str | None = None, icon: str | None = None
) -> None:
    """Add a new logging level to the logger.

    Args:
        name: The name of the new logging level.
        no: The numeric value of the new logging level.
        color: The color associated with the new logging level.
        icon: The icon associated with the new logging level.
    """
    with contextlib.suppress(ValueError):
        logger.level(name, no, color=color, icon=icon)
