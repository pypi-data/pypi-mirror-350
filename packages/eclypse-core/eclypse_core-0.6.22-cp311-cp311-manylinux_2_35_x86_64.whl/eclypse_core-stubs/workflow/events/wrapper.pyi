from typing import (
    Any,
    Callable,
)

from .event import EclypseEvent

class EventWrapper(EclypseEvent):
    """Class to wrap an event function into a class that can be managed by the
    Simulator."""

    def __init__(
        self,
        event_fn: Callable,
        name: str,
        trigger_every_ms: float | None = None,
        timeout: float | None = None,
        max_calls: int | None = None,
        triggers: dict[str, str | int | list[int]] | None = None,
        verbose: bool = False,
    ) -> None:
        """Initializes the EventWrapper.

        Args:
            event_fn (Callable): The event function to wrap.
            name (str): The name of the event.
            trigger_every_ms (Optional[float], optional): The time between triggers. Defaults to None.
            timeout (Optional[float], optional): The time after which the event times out. Defaults to None.
            max_calls (Optional[int], optional): The maximum number of times the event can be called. Defaults to None.
            triggers (Optional[Dict[str, Union[str, int, List[int]]]], optional): The triggers for the event. Defaults to None.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.
        """

    def __call__(self, **kwargs) -> dict[str, Any]: ...
