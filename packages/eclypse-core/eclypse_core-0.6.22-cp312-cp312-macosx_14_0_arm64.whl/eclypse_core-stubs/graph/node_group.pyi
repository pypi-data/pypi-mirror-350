from enum import Enum

class NodeGroup(Enum):
    """NodeGroup represents the group/layer of a node in the infrastructure. It is an enum
    with the following possible values:

    Attributes:
        UNSET: The node group is not set.
        IOT: The node group is an IoT device.
        EDGE: The node group is an edge device.
        CLOUD: The node group is a cloud server.
    """

    UNSET = ...
    IOT = ...
    FAR_EDGE = ...
    NEAR_EDGE = ...
    CLOUD = ...
    def __lt__(self, other: NodeGroup):
        """Return True if the value of the NodeGroup is less than the value of the other
        NodeGroup.

        Args:
            other (NodeGroup): The NodeGroup object to be compared with.

        Returns:
            bool: True if the current NodeGroup is less than the other, else False.
        """

    def __eq__(self, other: object):
        """Return True if the value of the NodeGroup is equal to the value of the.

        Args:
            other (NodeGroup): The NodeGroup object to be compared with.

        Returns:
            bool: True if the current NodeGroup is equal to the other, else False.
        """

    def __hash__(self): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
