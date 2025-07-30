from enum import Enum

class HTTPMethod(str, Enum):
    """HTTP methods supported by the `EclypseREST` communication interface.

    Attributes:
        GET: The GET HTTP method.
        POST: The POST HTTP method.
        PUT: The PUT HTTP method.
        DELETE: The DELETE HTTP method.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
