import abc
from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from eclypse_core.graph import (
    Application,
    Infrastructure,
)
from eclypse_core.placement import (
    Placement,
    PlacementView,
)

class PlacementStrategy(ABC, metaclass=abc.ABCMeta):
    """A global placement strategy that places services of an application on
    infrastructure nodes."""

    @abstractmethod
    def place(
        self,
        infrastructure: Infrastructure,
        application: Application,
        placements: dict[str, Placement],
        placement_view: PlacementView,
    ) -> dict[Any, Any]:
        """Given an infrastructure, an application, a dictionary of placements, and a
        placement view, return a mapping of services IDs to node IDs, for the
        application.

        This method must be overridden by the user.

        Args:
            infrastructure (Infrastructure): The infrastructure to place the application onto.
            application (Application): The application to place onto the infrastructure.
            placements (Dict[str, Placement]): A dictionary of placements.
            placement_view (PlacementView): The placement view to use for the placement.

        Returns:
            Dict[Any, Any]: A dictionary mapping service IDs to node IDs, or None if the application cannot be placed onto the infrastructure.
        """

    def is_feasible(
        self, infrastructure: Infrastructure, application: Application
    ) -> bool:
        """Check if the application can be placed on the infrastructure.

        Args:
            infrastructure (Infrastructure): The infrastructure to place the application onto.
            application (Application): The application to place onto the infrastructure.

        Returns:
            bool: True if the application can be placed on the infrastructure, False otherwise.
        """
