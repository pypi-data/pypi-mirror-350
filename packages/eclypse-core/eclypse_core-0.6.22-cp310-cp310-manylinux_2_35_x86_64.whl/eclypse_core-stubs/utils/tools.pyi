from typing import Any

__all__ = ["get_bytes_size", "get_constant", "camel_to_snake", "shield_interrupt"]

def get_bytes_size(d: Any) -> int:
    """Returns the size of an object in bytes.

    The size is computed according to the following rules:

    - int, float, str, bool: the size is the size of the object itself.
    - list, tuple, set: the size is the sum of the sizes of the elements in the collection.
    - dict: the size is the sum of the sizes of the keys and values in the dictionary.
    - objects with a __dict__ attribute: the size is the size of the __dict__ attribute.
    - other objects: the size is the size of the object itself, computed using `sys.getsizeof`.

    Args:
        d (Any): The object to be measured.

    Returns:
        int: The size of the object in bytes.
    """

def get_constant(name: str) -> Any:
    """Get the value of a constant in the `constants` module, given its name.

    Args:
        name (str): The name of the constant to retrieve

    Returns:
        Any: The value of the constant
    """

def camel_to_snake(s: str) -> str:
    """Convert a CamelCase string to a snake_case string.

    .. code-block:: python

            s = "MyCamelCaseSentence"
            print(camel_to_snake(s))  # my_camel_case_sentence

    Args:
        s (str): The CamelCase string to convert.

    Returns:
        str: The snake_case string.
    """

def shield_interrupt(func):
    """Decorator to catch the KeyboardInterrupt exception and stop the simulation.

    Args:
        func (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapped function with the KeyboardInterrupt exception handling.
    """
