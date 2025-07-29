import rich.pretty
import rich.traceback
from typing_extensions import deprecated

from liblaf.grapes import pretty


@deprecated("This function is deprecated and will be removed in a future version.")
def init_rich(*, show_locals: bool = True) -> None:
    """Initialize rich logging for pretty printing and tracebacks.

    This function sets up rich's pretty printing and traceback handling
    for the logging console.

    Args:
        show_locals: If True, local variables will be shown in tracebacks.
    """
    rich.pretty.install(console=pretty.get_console("stderr"))
    rich.traceback.install(
        console=pretty.get_console("stderr"), show_locals=show_locals
    )
