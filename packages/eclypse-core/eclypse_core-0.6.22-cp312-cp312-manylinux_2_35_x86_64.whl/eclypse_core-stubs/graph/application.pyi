from functools import cached_property
from typing import (
    Callable,
    Literal,
)

from networkx.classes.reportviews import (
    EdgeView,
    NodeView,
)

from eclypse_core.graph import AssetGraph
from eclypse_core.remote.service import Service

from .assets import Asset

class Application(AssetGraph):
    """Class to represent a multi-service Application."""

    services: dict[str, Service]
    def __init__(
        self,
        application_id: str,
        node_update_policy: (
            Callable[[NodeView], None] | list[Callable[[NodeView], None]] | None
        ) = None,
        edge_update_policy: (
            Callable[[EdgeView], None] | list[Callable[[EdgeView], None]] | None
        ) = None,
        node_assets: dict[str, Asset] | None = None,
        edge_assets: dict[str, Asset] | None = None,
        requirement_init: Literal["min", "max"] = "min",
        flows: list[list[str]] | None = None,
        seed: int | None = None,
    ) -> None:
        """Create a new Application.

        Args:
            application_id (str): The ID of the application.
            node_update_policy (Optional[Union[Callable[[NodeView], None], List[Callable[[NodeView], None]]]): The update policy for the services.
            edge_update_policy (Optional[Union[Callable[[EdgeView], None], List[Callable[[EdgeView], None]]]): The update policy for the interactions.
            node_assets (Optional[Dict[str, Asset]]): The assets of the nodes.
            edge_assets (Optional[Dict[str, Asset]]): The assets of the edges.
            include_default_assets (bool): Whether to include the default assets.
            requirement_init (Literal["min", "max"]): The initialization of the requirements.
            flows (Optional[List[List[str]]): The flows of the application.
            seed (Optional[int]): The seed for the random number generator.
        """

    def add_service(self, service: Service, **assets):
        """Add a service to the application.

        Args:
            service (Service): The service to add.
            **assets : The assets to add to the service.
        """

    def set_flows(self) -> None:
        """Set the flows of the application, using the following rules:

        - If the flows are already set, do nothing.
        - If the flows are not set, use the gateway as the source and all the other nodes as the target.
        - If there is no gateway, set the flows to an empty list.
        """

    @cached_property
    def has_logic(self) -> bool:
        """Check if the application has a logic for each service.

        This property requires to be True for the remote execution.
        """
