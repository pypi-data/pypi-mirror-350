"""Module containing type aliases used throughout the ECLYPSE package.

Attributes:

    HTTPMethodLiteral (Literal): Literal type for HTTP methods.\
        Possible values are ``"GET"``, ``"POST"``, ``"PUT"``, ``"DELETE"``.
    ConnectivityFn (Callable): Type alias for the connectivity function.\
        It takes two lists of strings and returns a generator of tuples of strings.
    CallbackType (Literal): Literal type for the callback types.\
        Possible values are ``"application"``, ``"infrastructure"``, ``"service"``,\
        ``"interaction"``, ``"node"``, ``"link"``, ``"simulation"``.
    PrimitiveType (Union): Type alias for primitive types.\
        Possible values are ``int``, ``float``, ``str``, ``bool``, ``list``,\
        ``tuple``, ``dict``, ``set``.
    PlotType (Literal): Literal type for the plot types.\
        Possible values are ``"bar"``, ``"line"``, ``"scatter"``.
    LogLevel (Literal): Literal type for the log levels.\
        Possible values are ``"TRACE"``, ``"DEBUG"``, ``"ECLYPSE"``, ``"INFO"``,\
        ``"SUCCESS"``, ``"WARNING"``, ``"ERROR"``, ``"CRITICAL"``.
"""

from __future__ import annotations

from typing import (
    Callable,
    Generator,
    List,
    Literal,
    Tuple,
    Union,
)

PrimitiveType = Union[int, float, str, bool, list, tuple, dict, set]

HTTPMethodLiteral = Literal[
    "GET",
    "POST",
    "PUT",
    "DELETE",
]

ConnectivityFn = Callable[
    [List[str], List[str]], Generator[Tuple[str, str], None, None]
]

CallbackType = Literal[
    "application",
    "infrastructure",
    "service",
    "interaction",
    "node",
    "link",
    "simulation",
]

LogLevel = Literal[
    "TRACE",
    "DEBUG",
    "ECLYPSE",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]
