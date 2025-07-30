import datetime as dt
from typing import (
    Any,
    Coroutine,
)

from eclypse_core.remote.communication.interface import (
    EclypseCommunicationInterface,
)
from eclypse_core.remote.service import Service

from .requests import (
    BroadcastRequest,
    MulticastRequest,
    UnicastRequest,
)

class EclypseMPI(EclypseCommunicationInterface):
    """The EclypseMPI implements the MPI communication protocol among services in the
    same application, deployed within the same infrastructure.

    It allows to send and receive messages among services, and to broadcast messages as
    well. The protocol is implemented by using the `MPIRequest` objects, which employ
    asynchrony to handle the simulation of communication costs of interactions.
    """

    def __init__(self, service: Service) -> None:
        """Initializes the MPI interface.

        Args:
            service (Service): The service that uses the MPI interface.
        """

    def send(
        self,
        recipient_ids: str | list[str],
        body: dict[str, Any],
        timestamp: dt.datetime | None = None,
    ) -> UnicastRequest | MulticastRequest:
        """Sends a message to a single recipient or multiple recipients. When awaited,
        the total wait time is the communication cost between the sender and the
        recipient in the case of a unicast, and the maximum communication cost among the
        interactions with the recipients in the case of a multicast. The result of this
        method **must be awaited**.

        Args:
            body (Any): The data to be sent. It must be a pickleable object.
            recipient_ids (Union[str, List[str], None]): The ids of the recipients. If a single id is specified, the message is sent to a single recipient. If a list of ids is specified, the message is sent to multiple recipients.

        Returns:
            Union[UnicastRequest, MulticastRequest]: The MPI request.
        """

    def bcast(
        self, body: Any, timestamp: dt.datetime | None = None
    ) -> BroadcastRequest:
        """Broadcasts a message to all neighbor services. When awaited, the total wait
        time is the maximum communication cost among the interactions with neighbors.
        The result of this method **must be awaited**.

        Args:
            body (Any): The data to be sent. It must be a pickleable object.
            timestamp (Optional[datetime.datetime], optional): The timestamp of the message. Defaults to datetime.datetime.now().

        Returns:
            BroadcastRequest: The Broadcast MPI request.
        """

    def recv(self) -> Coroutine[Any, Any, dict[str, Any]]:
        """Receive a message in the input queue. The result of this method **must be
        awaited**.

        Returns:
            Task[Any]: The message in the input queue.
        """

def exchange(*, receive: bool = False, send: bool = False, broadcast: bool = False):
    """Decorator to require and send a message in a Service method. The decorated
    function must receive, send, or broadcast a message. Sending and broadcasting are
    mutually exclusive.

    Args:
        receive (bool, optional): True if the decorated function receives a message.             Defaults to False.
        send (bool, optional): True if the decorated function sends a message.             Defaults to False.
        broadcast (bool, optional): True if the decorated function broadcasts a message.            Defaults to False.
    """
