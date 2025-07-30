from typing import (
    Callable,
    Literal,
)

import networkx as nx
from networkx.classes.reportviews import (
    EdgeView,
    NodeView,
)

from eclypse_core.graph.assets import Asset
from eclypse_core.utils._logging import Logger

class AssetGraph(nx.DiGraph):
    """AssetGraph represents an heterogeneous network infrastructure."""

    def __init__(
        self,
        graph_id: str,
        node_assets: dict[str, Asset] | None = None,
        edge_assets: dict[str, Asset] | None = None,
        node_update_policy: (
            Callable[[NodeView], None] | list[Callable[[NodeView], None]] | None
        ) = None,
        edge_update_policy: (
            Callable[[EdgeView], None] | list[Callable[[EdgeView], None]] | None
        ) = None,
        attr_init: Literal["min", "max"] = "min",
        flip_assets: bool = False,
        seed: int | None = None,
    ) -> None:
        """Initializes the AssetGraph object.

        Args:
            graph_id (str): The ID of the graph.
            node_assets (Optional[Dict[str, Asset]], optional): The assets of the nodes.                Defaults to None.
            edge_assets (Optional[Dict[str, Asset]], optional): The assets of the edges.                Defaults to None.
            node_update_policy (Optional[Callable[[NodeView], None]], optional): The policy to update the nodes. Defaults to None.
            edge_update_policy (Optional[Callable[[EdgeView], None]], optional): The policy to update the edges. Defaults to None.
            attr_init (Literal["min", "max"], optional): The initialization policy for the assets. Defaults to "min".
            flip_assets (bool, optional): Whether to flip the assets. Defaults to False.
            seed (Optional[int], optional): The seed for the random number generator.
                Defaults to None.
        """

    def add_node(self, node_for_adding: str, strict: bool = True, **assets):
        """Adds a node to the graph with the given assets. It also checks if the assets
        values are consistent with their spaces.

        Args:
            node_for_adding (Optional[str], optional): The node to add. Defaults to None.
            **assets: The assets of the node.
            strict (bool, optional): If True, raises an error if the assets are inconsistent.
                If False, logs a warning. Defaults to True.

        Raises:
            ValueError: If the assets are inconsistent and `strict` is True.
        """

    def add_edge(
        self,
        u_of_edge: str,
        v_of_edge: str,
        symmetric: bool = False,
        strict: bool = True,
        **assets
    ):
        """Adds an edge to the graph with the given assets. It also checks if the assets
        values are consistent with their spaces.

        Args:
            u_of_edge (str): The source node.
            v_of_edge (str): The target node.
            symmetric (bool, optional): If True, adds the edge in both directions.
                Defaults to False.
            strict (bool, optional): If True, raises an error if the assets are inconsistent.
                If False, logs a warning. Defaults to True.
            **assets: The assets of the edge.

        Raises:
            ValueError: If the source or target node is not found in the graph.
            ValueError: If the assets are inconsistent and `strict` is True.
        """

    def tick(self) -> None:
        """Updates the graph according to its update policies."""

    @property
    def is_dynamic(self) -> bool:
        """Checks if the graph is dynamic, i.e., if it has an update policy.

        Returns:
            bool: True if the graph is dynamic, False otherwise.
        """

    @property
    def logger(self) -> Logger:
        """Get a logger for the graph, binding the graph id in the logs.

        Returns:
            Logger: The logger for the graph.
        """
