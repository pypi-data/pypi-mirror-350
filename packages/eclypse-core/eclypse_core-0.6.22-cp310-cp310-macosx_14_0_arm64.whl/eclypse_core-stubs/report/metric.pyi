from typing import Callable

from eclypse_core.utils.types import CallbackType
from eclypse_core.workflow.callbacks import EclypseCallback

class EclypseMetric(EclypseCallback):
    """Class for a metric that will be used during the simulation for reporting
    purposes."""

    def __init__(
        self,
        name: str,
        callback_type: CallbackType | None = None,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = ...,
        aggregate_fn: str | Callable | None = None,
        remote: bool = False,
    ) -> None:
        """Initializes a metric object.

        Args:
            name (str): The name of the metric.
            callback_type (Optional[CallbackType], optional): The type of the callback. Defaults to None.
            activates_on (Union[str, List[str]], optional): The events that activate the callback. Defaults to "tick".
            activates_every_n (Optional[Dict[str, int]], optional): The number of times the callback is activated. Defaults to None.
            triggers (Optional[Dict[str, Callable]], optional): The triggers for the callback. Defaults to None.
            report (Optional[Union[str, List[str]]], optional): The type of report. Defaults to DEFAULT_REPORT_TYPE.
            aggregate_fn (Optional[Union[str, Callable]], optional): The aggregation function. Defaults to None.
            remote (bool, optional): Whether the callback is remote. Defaults to False.
        """

class EclypseMetricWrapper(EclypseMetric):
    """A class that wraps a function into a metric object, that can be managed by the
    Simulator."""

    def __init__(
        self,
        callback_fn: Callable,
        name: str,
        callback_type: CallbackType,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = ...,
        aggregate_fn: str | Callable | None = None,
        remote: bool = False,
    ) -> None:
        """Initializes a metric object.

        Args:
            callback_fn (Callable): The function to be wrapped.
            name (str): The name of the metric.
            callback_type (CallbackType): The type of the callback.
            activates_on (Union[str, List[str]], optional): The events that activate the callback. Defaults to "tick".
            activates_every_n (Optional[Dict[str, int]], optional): The number of times the callback is activated. Defaults to None.
            triggers (Optional[Dict[str, Callable]], optional): The triggers for the callback. Defaults to None.
            report (Optional[Union[str, List[str]]], optional): The type of report. Defaults to DEFAULT_REPORT_TYPE.
            aggregate_fn (Optional[Union[str, Callable]], optional): The aggregation function. Defaults to None.
            remote (bool, optional): Whether the callback is remote. Defaults to False.
        """

    def __call__(self, *args, **kwargs): ...
