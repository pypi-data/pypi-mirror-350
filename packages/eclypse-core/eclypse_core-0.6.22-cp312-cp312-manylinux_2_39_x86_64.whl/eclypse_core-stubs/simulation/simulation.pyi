from concurrent.futures import Future
from pathlib import Path
from typing import (
    Any,
    Generator,
)

from eclypse_core.graph import (
    Application,
    Infrastructure,
)
from eclypse_core.placement.strategy import PlacementStrategy
from eclypse_core.remote.bootstrap import RemoteBootstrap
from eclypse_core.simulation._simulator.local import (
    SimulationState,
    Simulator,
)
from eclypse_core.simulation._simulator.remote import RemoteSimulator
from eclypse_core.simulation.config import SimulationConfig
from eclypse_core.utils._logging import Logger

class Simulation:
    """A Simulation abstracts the deployment of applications on an infrastructure."""

    remote: RemoteBootstrap | None
    simulator: Simulator | RemoteSimulator
    def __init__(
        self,
        infrastructure: Infrastructure,
        simulation_config: SimulationConfig | None = None,
    ) -> None:
        """Create a new Simulation. It instantiates a Simulator or RemoteSimulator based
        on the simulation configuration, than can be either local or remote.

        It also registers an exit handler to ensure the simulation is properly closed
        and the reporting (if enabled) is done properly.

        Args:
            infrastructure (Infrastructure): The infrastructure to simulate.
            simulation_config (SimulationConfig, optional): The configuration of the simulation. Defaults to SimulationConfig().

        Raises:
            ValueError: If all services do not have a logic when including them in a remote
                simulation.
        """

    def start(self, blocking: bool = False):
        """Start the simulation."""

    def trigger(
        self, event_name: str, blocking: bool = True
    ) -> Future[dict[str, Any]] | dict[str, Any] | None:
        """Fire an event in the simulation.

        Args:
            event (str): The event to fire.
        """

    def feed(self, event_name: str) -> Generator[dict[str, Any], None, None]:
        """Feed the simulation with events.

        Args:
            event (str): The event to feed.
        """

    def tick(
        self, blocking: bool = True
    ) -> Future[dict[str, Any]] | dict[str, Any] | None:
        """Run a single tick of the simulation."""

    def stop(self, blocking: bool = True):
        """Stop the simulation."""

    def wait(self) -> None:
        """Wait for the simulation to finish.

        This method is blocking and will wait until the simulation is finished. It can
        be interrupted by pressing `Ctrl+C`.
        """

    def register(
        self,
        application: Application,
        placement_strategy: PlacementStrategy | None = None,
    ):
        """Include an application in the simulation.

        Args:
            application (Application): The application to include.
            placement_strategy (PlacementStrategy): The placement strategy to use to place the application on the infrastructure.

        Raises:
            ValueError: If all services do not have a logic when including them in a remote simulation.
        """

    @property
    def applications(self) -> list[Application]:
        """Get the applications in the simulation.

        Returns:
            List[Application]: The applications in the simulation.
        """

    @property
    def logger(self) -> Logger:
        """Get the logger of the simulation.

        Returns:
            EclypseLogger: The logger of the simulation.
        """

    @property
    def status(self) -> SimulationState:
        """Check if the simulation is stopped.

        Returns:
            bool: True if the simulation is stopped. False otherwise.
        """

    @property
    def path(self) -> Path:
        """Get the path to the simulation configuration.

        Returns:
            Path: The path to the simulation configuration.
        """
