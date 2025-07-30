import datetime as dt
from typing import (
    Any,
    Generator,
)

from eclypse_core.remote.communication.mpi import (
    EclypseMPI,
    Response,
)
from eclypse_core.remote.communication.mpi.requests import MulticastRequest
from eclypse_core.remote.communication.route import Route

class UnicastRequest(MulticastRequest):
    """A request to send a message to a single recipient."""

    def __init__(
        self,
        recipient_id: str,
        body: dict[str, Any],
        _mpi: EclypseMPI,
        timestamp: dt.datetime | None = None,
    ) -> None:
        """Initializes a UnicastRequest object.

        Args:
            recipient_id (str): The ID of the recipient node.
            body (Dict[str, Any]): The body of the request.
            _mpi (EclypseMPI): The MPI interface.
        """

    def __await__(self) -> Generator[Any, None, UnicastRequest]:
        """Await the request to complete.

        Returns:
            Awaitable: The result of the request.
        """

    @property
    def recipient_id(self) -> str:
        """The ID of the recipient.

        Returns:
            str: The ID.
        """

    @property
    def response(self) -> Response | None:
        """The response to the request.

        Returns:
            Optional[Response]: The response to the request if available, None otherwise.
        """

    @property
    def route(self) -> Route | None:
        """The route to the recipient.

        Returns:
            Optional[Route]: The route to the recipient if available, None otherwise.
        """

    @property
    def elapsed_time(self) -> dt.timedelta | None:
        """The elapsed time until the response was received.

        Returns:
            Optional[timedelta]: The elapsed time until the response was received,
                or None if the response is not yet available.
        """
