from typing import Callable

from eclypse_core.remote.communication.interface import (
    EclypseCommunicationInterface,
)
from eclypse_core.remote.service import Service
from eclypse_core.utils.types import HTTPMethodLiteral

from .methods import HTTPMethod

class EclypseREST(EclypseCommunicationInterface):
    """The EclypseREST implements the REST communication interface among services in the
    same application, deployed within the same infrastructure.

    It allows to send and receive HTTP requests at specific endpoints, which are defined
    by each service, using the @endpoint decorator.
    """

    endpoints: dict[str, dict[HTTPMethod, Callable]]
    def __init__(self, service: Service) -> None:
        """Initializes the REST interface.

        Args:
            service (Service): The service that uses the REST interface.
        """

    def connect(self) -> None:
        """Connects the REST interface to the service, registering the endpoints and
        their handlers."""

    def disconnect(self) -> None:
        """Disconnects the REST interface from the service, clearing the endpoints."""

    def get(self, url: str, **data):
        """Creates and handles a GET request.

        Args:
            url (str): The URL of the request.
            **data: The data to be sent in the request.
        """

    def post(self, url: str, **data):
        """Creates and handles a POST request.

        Args:
            url (str): The URL of the request.
            **data: The data to be sent in the request.
        """

    def put(self, url: str, **data):
        """Creates and handles a PUT request.

        Args:
            url (str): The URL of the request.
            **data: The data to be sent in the request.
        """

    def delete(self, url: str, **data):
        """Creates and handles a DELETE request.

        Args:
            url (str): The URL of the request.
            **data: The data to be sent in the request.
        """

def register_endpoint(endpoint: str, method: HTTPMethod | HTTPMethodLiteral):
    """Decorator to register an endpoint in a service.

    Args:
        endpoint (str): The endpoint to register.
        methods (List[HTTPMethod]): The methods allowed for the endpoint.

    Returns:
        Callable: The decorated function.
    """
