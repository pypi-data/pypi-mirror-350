import asyncio
from typing import Literal

from eclypse_core.remote.communication.mpi import EclypseMPI
from eclypse_core.remote.communication.rest import EclypseREST
from eclypse_core.utils._logging import Logger

class Service:
    """Base class for services in ECLYPSE remote applications."""

    def __init__(
        self,
        service_id: str,
        comm_interface: Literal["mpi", "rest"] = "mpi",
        store_step: bool = False,
    ) -> None:
        """Initializes a Service object.

        Args:
            service_id (str): The name of the service.
            comm_interface (Literal["mpi", "rest"], optional): The communication interface
                of the service. Defaults to "mpi".
            store_step (bool, optional): Whether to store the results of each step. Defaults
                to False.
        """

    async def run(self) -> None:
        """Runs the service. It provides a default behaviour where the service runs the
        `step` method in a loop until the service is stopped.

        This method can be overridden by the user to provide a custom behaviour.
        """

    async def step(self) -> None:
        """The service's main loop.

        This method must be overridden by the user.

        Returns:
            Any: The result of the step (if any).

        Raises:
            NotImplementedError: If the method is not overridden.
        """

    def on_deploy(self) -> None:
        """Hook called when the service is deployed on a node."""

    def on_undeploy(self) -> None:
        """Hook called when the service is undeployed from a node."""

    @property
    def mpi(self) -> EclypseMPI:
        """Returns the EclypseMPI interface of the service."""

    @property
    def rest(self) -> EclypseREST:
        """Returns the EclypseREST interface of the service."""

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """Returns the asyncio event loop of the service."""

    @property
    def id(self):
        """Returns the ID of the service, with the format application_id/service_id."""

    @property
    def application_id(self):
        """Returns the ID of the application the service belongs to."""

    @application_id.setter
    def application_id(self, application_id: str):
        """Sets the ID of the application the service belongs to."""

    @property
    def deployed(self):
        """Returns True if the service is deployed on a node."""

    @property
    def running(self):
        """Returns True if the service is running."""

    @property
    def logger(self) -> Logger:
        """Returns the logger of the service, binding the service ID in the logs.

        Returns:
            Logger: The logger fo the Service.
        """
