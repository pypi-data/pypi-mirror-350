from typing import (
    Any,
    Generator,
)

from eclypse_core.remote.communication import (
    EclypseRequest,
    Route,
)

from .codes import HTTPStatusCode
from .interface import EclypseREST
from .methods import HTTPMethod

class HTTPRequest(EclypseRequest):
    """An HTTP request object, used to send and receive data between services in the
    same application, using the REST communication protocol."""

    def __init__(
        self, url: str, method: HTTPMethod, data: dict[Any, Any], _rest: EclypseREST
    ) -> None:
        """Initializes an HTTPRequest object.

        Args:
            url (str): The URL of the request.
            method (HTTPMethod): The HTTP method of the request.
            data (Dict[Any, Any]): The data to send in the request.
            _rest (EclypseREST): The REST interface used to send the request.
        """

    def __await__(self) -> Generator[Any, None, HTTPRequest]:
        """Await the request to complete.

        Returns:
            Awaitable: The result of the request.
        """

    @property
    def route(self) -> Route | None:
        """Get the route of the request.

        Returns:
            Optional[Route]: The route of the request.
        """

    @property
    def response(self) -> tuple[HTTPStatusCode, dict[str, Any]] | None:
        """Get the response of the request.

        Returns:
            Tuple[HTTPStatusCode, Dict[str, Any]]: The response of the request.
        """

    @property
    def status_code(self) -> HTTPStatusCode:
        """Get the status code of the response.

        Returns:
            HTTPStatusCode: The status code of the response.

        Raises:
            RuntimeError: If the request is not completed yet.
        """

    @property
    def body(self) -> dict[str, Any]:
        """Get the body of the response.

        Returns:
            Dict[str, Any]: The body of the response.

        Raises:
            RuntimeError: If the request is not completed yet.
        """
