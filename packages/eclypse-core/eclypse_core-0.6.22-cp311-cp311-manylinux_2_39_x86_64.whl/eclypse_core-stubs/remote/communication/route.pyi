from typing import Any

class Route:
    """A route which connects two neighbor services in an application.

    It contains the sender and recipient IDs, the sender and recipient node IDs, the
    list of hops (i.e., triplets denoting source node of the hop, target node of the
    hop, and cost of the link).
    """

    def __init__(
        self,
        sender_id: str,
        sender_node_id: str,
        recipient_id: str,
        recipient_node_id: str,
        processing_time: float,
        hops: list[tuple[str, str, dict[str, Any]]] | None = None,
    ) -> None:
        """Initializes a Route object.

        Args:
            sender_id (str): The ID of the sender service.
            sender_node_id (str): The ID of the node where the sender service is deployed.
            recipient_id (str): The ID of the recipient service.
            recipient_node_id (str): The ID of the node where the recipient service is deployed.
            processing_time (float): The processing time of the nodes traversed by the route.
            hops (Optional[List[Tuple[str, str, Dict[str, Any]]]]): The list of hops in the route. Each hop is a triplet containing the source node ID, the target node ID, and the cost of the link. Defaults to None.
        """

    def __len__(self) -> int:
        """Returns the number of hops in the route.

        Returns:
            int: The number of hops.
        """

    def cost(self, msg: Any) -> float:
        """Returns a function that computes the cost of the route for a given object.

        The object must be dict-like (i.e., it must have a __dict__ method).

        Args:
            msg (Any): The object for which to compute the cost (e.g., a message).

        Returns:
            float: The function that computes the cost of the route.
        """

    @property
    def network_cost(self):
        """Returns the network cost of the route.

        The network cost is computed as the sum of the costs of the links in the route.

        Returns:
            float: The network cost.
        """

    @property
    def no_hop(self) -> bool:
        """Returns True if the sender and recipient are deployed on the same node.

        Returns:
            bool: True if the sender and recipient are deployed on the same node, False otherwise.
        """
