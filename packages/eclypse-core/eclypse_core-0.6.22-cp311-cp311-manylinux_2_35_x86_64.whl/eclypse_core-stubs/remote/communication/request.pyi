import datetime as dt
from typing import (
    Any,
    Generator,
)

from .interface import EclypseCommunicationInterface
from .route import Route

class EclypseRequest:
    """Class for an Eclypse request."""

    def __init__(
        self,
        recipient_ids: list[str],
        data: dict[str, Any],
        _comm: EclypseCommunicationInterface,
        timestamp: dt.datetime | None = None,
    ) -> None:
        """Create a new EclypseRequest.

        Args:
            recipient_ids (List[str]): The ids of the recipients.
            data (Dict[str, Any]): The data of the request.
            _comm (EclypseCommunicationInterface): The communication interface.
            timestamp (Optional[dt.datetime], optional): The timestamp of the request.
                Defaults to None.
        """

    def __await__(self) -> Generator[Any, None, EclypseRequest]:
        """Await the request to complete.

        Returns:
            Awaitable: The result of the request.
        """

    @property
    def data(self) -> dict[str, Any]:
        """Get the data of the request.

        Returns:
            Dict[str, Any]: The data.
        """

    @property
    def timestamp(self) -> dt.datetime:
        """Get the timestamp of the request.

        Returns:
            dt.datetime: The timestamp.
        """

    @property
    def recipient_ids(self) -> list[str]:
        """The ids of the recipients.

        Returns:
            List[str]: The ids.
        """

    @property
    def routes(self) -> list[Route | None]:
        """Wait for the routes to be computed.

        This method can be awaited explicitly to
        compute the routes to the recipients. Otherwise, it is awaited implicitly when
        the `EclypseRequest` object is awaited to process the request.
        """

    @property
    def responses(self) -> list[Any | None]:
        """Wait for the responses to the MPI request.

        This method can be called explicitly to wait for the responses to the EclypseRequest
        Otherwise, it is called implicitly when the `EclypseRequest` object is awaited to
        process the request.
        """

    @property
    def elapsed_times(self) -> list[dt.timedelta | None]:
        """The elapsed times until the responses were received.

        Returns:
            List[timedelta]: The elapsed times until the responses were received.
                If a response is not yet available, a timedelta of 0 is returned
                for the corresponding recipient.
        """
