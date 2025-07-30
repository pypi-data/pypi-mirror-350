from typing import (
    Any,
    Callable,
    Literal,
)

import networkx as nx
from networkx.classes.reportviews import (
    EdgeView,
    NodeView,
)

from eclypse_core.graph import AssetGraph
from eclypse_core.graph.assets.asset import Asset
from eclypse_core.placement.strategy import PlacementStrategy

class Infrastructure(AssetGraph):
    """Class to represent a Cloud-Edge infrastructure."""

    def __init__(
        self,
        infrastructure_id: str = "Infrastructure",
        placement_strategy: PlacementStrategy | None = None,
        node_update_policy: (
            Callable[[NodeView], None] | list[Callable[[NodeView], None]] | None
        ) = None,
        edge_update_policy: (
            Callable[[EdgeView], None] | list[Callable[[EdgeView], None]] | None
        ) = None,
        node_assets: dict[str, Asset] | None = None,
        edge_assets: dict[str, Asset] | None = None,
        path_assets_aggregators: dict[str, Callable[[list[Any]], Any]] | None = None,
        path_algorithm: Callable[[nx.Graph, str, str], list[str]] | None = None,
        resource_init: Literal["min", "max"] = "min",
        seed: int | None = None,
    ) -> None:
        """Create a new Infrastructure.

        Args:
            infrastructure_id (str): The ID of the infrastructure.
            placement_strategy (Optional[PlacementStrategy]): The placement strategy to use.
            node_update_policy (Optional[Union[Callable[[NodeView], None], List[Callable[[NodeView], None]]]]): A function to update the nodes.
            edge_update_policy (Optional[Union[Callable[[EdgeView], None], List[Callable[[EdgeView], None]]]]): A function to update the edges.
            node_assets (Optional[Dict[str, Asset]]): The assets of the nodes.
            edge_assets (Optional[Dict[str, Asset]]): The assets of the edges.
            path_assets_aggregators (Optional[Dict[str, Callable[[List[Any]], Any]]]): The aggregators to use for the path assets.
            path_algorithm (Optional[Callable[[nx.Graph, str, str], List[str]]]): The algorithm to use to compute the paths.
            resource_init (Literal["min", "max"]): The initialization method for the resources.
            seed (Optional[int]): The seed for the random number generator.
        """

    def contains(self, other: nx.DiGraph) -> list[str]:
        """Compares the requirements of the nodes and edges in the PlacementView with
        the resources of the nodes and edges in the Infrastructure.

        Args:
            other (Infrastructure): The Infrastructure to compare with.

        Returns:
            List[str]: A list of nodes whose requirements are not respected or whose connected links are not respected.
        """

    def path(
        self, source: str, target: str
    ) -> tuple[list[tuple[str, str, dict[str, Any]]], float] | None:
        """Retrieve the path between two nodes, if it exists. If the path does not
        exist, it is computed and cached, with costs for each hop. Both the path and the
        costs are recomputed if any of the hop costs has changed by more than 5%.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.

        Returns:
            Optional[List[Tuple[str, str, float]]]: The path between the two nodes in the form (source, target, cost), or None if the path does not exist.
        """

    def path_resources(self, source: str, target: str) -> dict[str, Any]:
        """Retrieve the resources of the path between two nodes, if it exists. If the
        path does not exist, it is computed and cached.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.

        Returns:
            PathResources: The resources of the path between the two nodes, or None if the path does not exist.
        """

    @property
    def available(self) -> Infrastructure:
        """Return the subgraph with only the available nodes.

        Returns:
            nx.DiGraph: A subgraph with only the available nodes, named "av-{id}".
        """

    def is_available(self, n: NodeView):
        """Check if the node is available.

        Args:
            n (NodeView): The node to check.

        Returns:
            bool: True if the node is available, False otherwise.
        """

    @property
    def has_strategy(self) -> bool:
        """Check if the infrastructure has a placement strategy.

        Returns:
            bool: True if the infrastructure has a placement strategy, False otherwise.
        """
