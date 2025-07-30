from functools import cached_property
from typing import (
    Any,
    Callable,
)

import networkx as nx

from eclypse_core.graph import Infrastructure
from eclypse_core.graph.assets import AssetBucket

class PlacementView(nx.DiGraph):
    """PlacementView is a snapshot of the required resources of an Infrastructure."""

    nodes_used_by: dict[str, set[str]]
    def __init__(self, infrastructure: Infrastructure) -> None:
        """Initializes the PlacementView."""

    def get_node_view(self, node_name: str) -> dict[str, Any]:
        """Gets the resources required on a node.

        Args:
            node (str): The name of the node.

        Returns:
            ServiceRequirements: The resources required on the node.
        """

    def get_edge_view(self, source: str, target: str) -> dict[tuple[str, str], Any]:
        """Gets the resources required on a link.

        Args:
            source (str): The source node of the link.
            target (str): The target node of the link.

        Returns:
            S2SRequirements: The resources required on the link.
        """

    @cached_property
    def node_aggregate(self) -> Callable[..., dict[str, Any]]:
        """Returns a function that aggregates the resources required on a node.

        Returns:
            Callable[..., Dict[str, Any]]: The function that aggregates the resources.
        """

    @cached_property
    def edge_aggregate(self) -> Callable[..., dict[str, Any]]:
        """Returns a function that aggregates the resources required on a link.

        Returns:
            Callable[..., Dict[str, Any]]: The function that aggregates the resources.
        """

    @property
    def node_assets(self) -> AssetBucket:
        """Alias for the node assets of the infrastructure.

        Returns:
            AssetBucket: The node assets of the infrastructure.
        """

    @property
    def edge_assets(self) -> AssetBucket:
        """Alias for the edge assets of the infrastructure.

        Returns:
            AssetBucket: The edge assets of the infrastructure.
        """
