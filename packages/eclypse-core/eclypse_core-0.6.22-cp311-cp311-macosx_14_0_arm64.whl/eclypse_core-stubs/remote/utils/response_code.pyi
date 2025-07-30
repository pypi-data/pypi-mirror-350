from enum import Enum

class ResponseCode(Enum):
    """A ResponseCode is an enumeration denoting possible responses to an
    `EclypseRequest`.

    Attributes:
        OK: The request was processed successfully.
        ERROR: An error occurred while processing the request.
    """

    OK = ...
    ERROR = ...
