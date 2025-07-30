import datetime as dt
from typing import (
    Any,
    Generator,
)

from eclypse_core.remote.communication.mpi import EclypseMPI

from .multicast import MulticastRequest

class BroadcastRequest(MulticastRequest):
    """Request for broadcasting a message to all neighbor services in the network."""

    def __init__(
        self,
        body: dict[str, Any],
        _mpi: EclypseMPI,
        timestamp: dt.datetime | None = None,
    ) -> None:
        """Initializes a BroadcastRequest object.

        Args:
            body (Dict[str, Any]): The body of the request.
            _mpi (EclypseMPI): The MPI interface.
        """

    def __await__(self) -> Generator[Any, None, BroadcastRequest]:
        """Await the request to complete.

        Returns:
            Awaitable: The result of the request.
        """
