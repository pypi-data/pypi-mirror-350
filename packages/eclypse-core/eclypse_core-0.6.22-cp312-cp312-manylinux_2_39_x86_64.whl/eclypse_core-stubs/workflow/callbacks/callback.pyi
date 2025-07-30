from typing import (
    Any,
    Callable,
)

from eclypse_core.utils.types import CallbackType

class EclypseCallback:
    """A callback object that is called at every simulation tick or at the end of the
    simulation."""

    def __init__(
        self,
        name: str,
        callback_type: CallbackType | None = None,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = ...,
        remote: bool = False,
    ) -> None:
        """Initialize the Callback object.

        Args:
            callback_fn (Callable): The callback function.
            callback_type (CallbackType): The type of the callback, used to determine the type of value it manages.
            activates_on (Union[str, List[str]]): The event(s) that trigger the callback.
            activates_every_n (Optional[Dict[str, int]]): The number of ticks between each call to the callback function.
            triggers (Optional[Dict[str, Callable]]): The condition to trigger the callback.
            report (Optional[Union[str, List[str]]]): The type of report to generate. Defaults to DEFAULT_REPORT_TYPE.
            remote (bool): Whether the simulation is local or remote (emulation), thus running using ray.
            name (Optional[str]): The name of the callback.
        """

    def __call__(self, *args, **kwargs) -> dict[str, Any]: ...
    @property
    def name(self) -> str:
        """The name of the callback.

        Returns:
            str: The name of the callback.
        """

    @property
    def n_calls(self) -> dict[str, int]:
        """The number of times the callback was called.

        Returns:
            Dict[str, int]: The number of times the callback was called.
        """

    @property
    def data(self) -> Any | None:
        """The value returned by the callback function.

        Returns:
            Optional[Any]: The value returned by the callback function, if any.
        """

    @property
    def type(self) -> CallbackType | None:
        """The type of the callback.

        Returns:
            CallbackType: The type of the callback.
        """

    @property
    def activates_on(self) -> list[str]:
        """The events that trigger the callback.

        Returns:
            Union[List[str]]: The events that trigger the callback.
        """

    @property
    def activated_by(self) -> str | None:
        """Whether the callback was triggered.

        Returns:
            bool: True if the callback was triggered, False otherwise.
        """

    @activated_by.setter
    def activated_by(self, value: str | None): ...
    @property
    def report_types(self) -> list[str]:
        """The type of the report.

        Returns:
            str: The type of the report.
        """

    @property
    def remote(self) -> bool:
        """Whether the callback is local or remote (emulation).

        Returns:
            bool: True if the callback is remote, False otherwise.
        """
