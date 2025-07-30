from typing import Any

from eclypse_core.graph.application import Application
from eclypse_core.graph.infrastructure import Infrastructure

from .strategy import PlacementStrategy

class Placement:
    """A placement is a mapping of each service of an application to a node of an
    infrastructure, computed according to a placement strategy."""

    strategy: PlacementStrategy | None
    infrastructure: Infrastructure
    application: Application
    mapping: dict[str, str]
    def __init__(
        self,
        infrastructure: Infrastructure,
        application: Application,
        strategy: PlacementStrategy | None = None,
    ) -> None:
        """Initializes the Placement.

        Args:
            infrastructure (Infrastructure): The infrastructure to place the application onto.
            application (Application): The application to place onto the infrastructure.
            strategy (PlacementStrategy): The strategy to use for the placement.
        """

    def service_placement(self, service_id: str) -> str:
        """Return the node where a service is placed.

        Args:
            service_id (str): The name of the service.

        Returns:
            str: The name of the node where the service is placed.
        """

    def services_on_node(self, node_name: str) -> list[str]:
        """Return all the services placed on a node.

        Args:
            node_name (str): The name of the node.

        Returns:
            List[str]: The names of the services placed on the node.
        """

    def interactions_on_link(self, source: str, target: str) -> list[tuple[str, str]]:
        """Return all the services interactions crossing a link.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.

        Returns:
            List[Tuple[str, str]]: The names of the services interactions crossing the link.
        """

    def node_service_mapping(self) -> dict[str, list[str]]:
        """Return a view of the placement as a mapping of nodes to the list of services
        placed on them."""

    def link_interaction_mapping(self) -> dict[tuple[str, str], list[tuple[str, str]]]:
        """Return a view of the placement as a mapping of links to the list of services
        interactions crossing them.

        Returns:
            Dict[Tuple[str, str], List[Tuple[str, str]]]: The mapping of links to the list of services interactions crossing them.
        """

    def node_requirements_mapping(self) -> dict[str, dict[str, Any]]:
        """Return a view of the placement as a mapping of nodes to the total
        requirements of the services placed on them.

        Returns:
            Dict[str, ServiceRequirements]: The mapping of nodes to the total requirements of the services placed on them.
        """

    def link_requirements_mapping(self) -> dict[tuple[str, str], dict[str, Any]]:
        """Return a view of the placement as a mapping of links to the total
        requirements of the services interactions crossing them.

        Returns:
            Dict[Tuple[str, str], S2SRequirements]: The mapping of links to the total requirements of the services interactions crossing them.
        """

    @property
    def is_partial(self) -> list[str]:
        """Return whether the placement is partial or not.

        Returns:
            List[str]: The list of services that are not placed.
        """
