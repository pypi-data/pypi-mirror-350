from typing import Callable

from eclypse_core.utils.types import CallbackType

def generic(
    fn_or_class: Callable | None = None,
    *,
    callback_type: CallbackType | None = None,
    activates_on: str | list[str] = "tick",
    activates_every_n: dict[str, int] | None = None,
    triggers: dict[str, Callable] | None = None,
    report: str | list[str] | None = None,
    remote: bool = False,
    name: str | None = None
) -> Callable:
    """A decorator that defines a named function as a callback.

    Args:
        fn_or_class (Optional[Callable], optional): The function or class to decorate             as a callback. Defaults to None.
        callback_type (Optional[CallbackType], optional): The type of callback.             Defaults to None.
        activates_on (Union[str, List[str]], optional): The event that triggers the             callback. Defaults to "tick".
        activates_every_n (Optional[Dict[str, int]], optional): The number of times the             callback is activated. Defaults to None.
        triggers (Optional[Dict[str, Callable]], optional): The functions that trigger             the callback. Defaults to None.
        report (Optional[Union[str, List[str]], optional):             The type(s) of reporter to use for reporting the callback. Defaults to None.

    Returns:
        Callable: The decorated function.
    """
