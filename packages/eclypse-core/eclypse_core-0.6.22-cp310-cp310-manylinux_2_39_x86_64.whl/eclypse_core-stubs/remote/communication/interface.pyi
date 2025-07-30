from asyncio import (
    Future,
    Task,
)

from eclypse_core.remote.service import Service

from .route import Route

class EclypseCommunicationInterface:
    """The EclypseCommunicationInterface is used to implement and simulate the
    interactions between services deployed and running in the same infrastructure.

    It allows to interact with the `RemoteSimulator`, which provides the details regarding
    the current state of the infrastructure, and simulate the behaviour of the services
    accordingly.
    """

    def __init__(self, service: Service) -> None:
        """Initializes the communication interface.

        Args:
            service (Service): The service that uses the communication interface.
        """

    def connect(self) -> None:
        """Connects the communication interface to the `RemoteSimulator`."""

    def disconnect(self) -> None:
        """Disconnects the communication interface from the `RemoteSimulator`."""

    def request_route(self, recipient_id: str) -> Future[Route]:
        """Interacts with the `RemoteSimulator` to request a route to a desired
        recipient service. The result of the function can be obtained by calling
        `ray.get` or by awaiting it.

        Args:
            recipient_id (str): The ID of the recipient service.

        Returns:
            Task[Route]: The route to the recipient service.
        """

    def get_neighbors(self) -> Task[list[str]]:
        """Interacts with the InfrastructureManager to request the list of neighbors of
        the service. The result of the function can be obtained by calling `ray.get` or
        by awaiting it.

        Returns:
            Task[List[str]]: The list of neighbor service IDs.
        """

    @property
    def connected(self) -> bool:
        """Returns True if the communication interface is connected to the
        RemoteSimulator.

        Returns:
            bool: True if the communication interface is connected.
        """

    @property
    def service(self) -> Service:
        """Returns the service leveraging the communication interface.

        Returns:
            Service: The service leveraging the communication interface.
        """
