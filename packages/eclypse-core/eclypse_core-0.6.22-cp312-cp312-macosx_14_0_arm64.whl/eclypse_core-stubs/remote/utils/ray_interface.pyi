from typing import Any

from ray import ObjectRef
from ray.actor import ActorHandle

class RayInterface:
    def __init__(self) -> None: ...
    def init(self, runtime_env: dict[str, Any]): ...
    def get(self, obj: ObjectRef) -> Any:
        """Get the result of a Ray task or a list of Ray tasks, ignoring any output to
        stderr.

        Args:
            Any: The Ray task or list of Ray tasks.

        Returns:
            Union[Any, List[Any]]: The result of the Ray task or list of Ray tasks.
        """

    def put(self, obj: Any) -> ObjectRef: ...
    def get_actor(self, name: str) -> ActorHandle: ...
    def remote(self, fn_or_class): ...
    @property
    def backend(self): ...
