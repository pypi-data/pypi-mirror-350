import datetime as dt

from eclypse_core.remote.utils import ResponseCode

class Response:
    """A Response is a data structure for acknowledging the processing of a message
    exchange within an `MPIRequest`."""

    def __init__(self, code: ResponseCode = ..., timestamp: dt.datetime = ...) -> None:
        """Initializes a Response object.

        Args:
            code (ResponseCode): The response code.
            timestamp (datetime.datetime): The timestamp of the response.
        """
