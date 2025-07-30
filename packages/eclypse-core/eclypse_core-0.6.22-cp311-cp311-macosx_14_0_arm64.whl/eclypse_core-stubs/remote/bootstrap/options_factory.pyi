from typing import Any

class RayOptionsFactory:
    """Factory for creating Ray options for remote nodes."""

    def __init__(self, detached: bool = False, **ray_options) -> None:
        """Create a new RayOptionsFactory.

        Args:
            detached (bool, optional): Whether to run the actor detached. Defaults to False.
            **ray_options: The options for Ray. See the documentation `here <https://docs.ray.io/en/latest/ray-core/api/doc/ray.remote.html#ray.remote>`_ for more information.
        """

    def __call__(self, name: str) -> dict[str, Any]:
        """Create the options for the actor.

        Args:
            name (str): The name of the actor.

        Returns:
            Dict[str, Any]: The options for the actor.
        """
