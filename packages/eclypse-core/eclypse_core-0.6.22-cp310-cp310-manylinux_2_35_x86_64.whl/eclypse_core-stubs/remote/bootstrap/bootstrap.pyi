from eclypse_core.graph.infrastructure import Infrastructure
from eclypse_core.remote._node import RemoteNode
from eclypse_core.simulation._simulator.remote import RemoteSimulator
from eclypse_core.simulation.config import SimulationConfig

from .options_factory import RayOptionsFactory

class RemoteBootstrap:
    """Configuration for the remote infrastructure."""

    env_vars: dict[str, str]
    def __init__(
        self,
        sim_class: type[RemoteSimulator] | None = None,
        node_class: type[RemoteNode] | None = None,
        ray_options_factory: RayOptionsFactory | None = None,
        **node_args
    ) -> None:
        """Create a new RemoteBootstrap.

        Args:
            sim_class (Optional[Type[RemoteSimulator]]): The remote simulator class.
            node_class (Optional[Type[RemoteNode]]): The remote node class.
            ray_options_factory (Optional[RayOptionsFactory]): The Ray options factory.
            resume_if_exists (bool): Whether to resume the simulation if it exists.
            **node_args: The arguments for the remote node.
        """

    def build(
        self,
        infrastructure: Infrastructure,
        simulation_config: SimulationConfig | None = None,
    ):
        """Build the remote simulation."""
