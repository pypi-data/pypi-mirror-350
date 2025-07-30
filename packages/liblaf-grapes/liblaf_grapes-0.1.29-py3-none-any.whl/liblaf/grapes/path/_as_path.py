from pathlib import Path

from liblaf.grapes.typed import PathLike


def as_path(path: PathLike, *, expend_user: bool = True) -> Path:
    path = Path(path)
    if expend_user:
        path = path.expanduser()
    return path
