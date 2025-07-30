from typing import (
    Any,
    Callable,
)

from eclypse_core.utils.types import CallbackType

from .callback import EclypseCallback

class CallbackWrapper(EclypseCallback):
    """Class to wrap a callback function into a class that can be managed by the
    Simulator."""

    def __init__(
        self,
        callback_fn: Callable,
        name: str,
        callback_type: CallbackType | None = None,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = ...,
        remote: bool = False,
    ) -> None:
        """Initializes the CallbackWrapper.

        Args:
            callback_fn (Callable): The callback function to wrap.
            name (str): The name of the callback.
            callback_type (Optional[CallbackType], optional): The type of the callback. Defaults to None.
            activates_on (Union[str, List[str]], optional): The event(s) that activate the callback. Defaults to "tick".
            activates_every_n (Optional[Dict[str, int]], optional): The number of times the callback activates. Defaults to None.
            triggers (Optional[Dict[str, Callable]], optional): The triggers for the callback. Defaults to None.
            report (Optional[Union[str, List[str]]], optional): The report(s) to generate. Defaults to DEFAULT_REPORT_TYPE.
            remote (bool, optional): Whether the callback is remote. Defaults to False.
        """

    def __call__(self, *args, **kwargs) -> dict[str, Any]: ...
