import abc
from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
from typing import Any

from eclypse_core.workflow.callbacks import EclypseCallback

class Reporter(ABC, metaclass=abc.ABCMeta):
    """Abstract class to report the simulation metrics.

    It provides the interface for the simulation reporters.
    """

    def __init__(self, report_path: str | Path) -> None:
        """Create a new Reporter.

        Args:
            report_path (Union[str, Path]): The path to save the reports.
        """

    @abstractmethod
    def report(
        self,
        event_name: str,
        event_idx: int,
        executed: list[EclypseCallback],
        *args,
        **kwargs
    ):
        """Report the simulation reportable callbacks.

        Args:
            event_name (str): The name of the event.
            event_idx (int): The index of the event trigger (tick).
            executed (List[EclypseCallback]): The executed callbacks.
        """

    def dfs_data(self, data: Any) -> list:
        """Perform DFS on the nested dictionary and build paths (concatenated keys) as
        strings.

        Args:
            data (Any): The data to traverse.

        Returns:
            List: The list of paths.
        """
