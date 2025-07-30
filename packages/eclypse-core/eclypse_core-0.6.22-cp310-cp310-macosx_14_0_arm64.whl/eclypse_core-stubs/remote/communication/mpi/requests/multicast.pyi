import datetime as dt
from typing import (
    Any,
    Generator,
)

from eclypse_core.remote.communication import EclypseRequest
from eclypse_core.remote.communication.mpi import EclypseMPI

class MulticastRequest(EclypseRequest):
    """A request to send a message to multiple recipients."""

    def __init__(
        self,
        recipient_ids: list[str],
        body: dict[str, Any],
        _mpi: EclypseMPI,
        timestamp: dt.datetime | None = None,
    ) -> None:
        """Initializes a MulticastRequest object.

        Args:
            recipient_ids (List[str]): The IDs of the recipient nodes.
            body (Dict[str, Any]): The body of the request.
            _mpi (EclypseMPI): The MPI interface.
            timestamp (Optional[dt.datetime], optional): The timestamp of the request.
                Defaults to None.
        """

    def __await__(self) -> Generator[Any, None, MulticastRequest]:
        """Await the request to complete.

        Returns:
            Awaitable: The result of the request.
        """
