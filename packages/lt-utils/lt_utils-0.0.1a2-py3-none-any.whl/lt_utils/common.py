__all__ = [
    "ABC",
    "abstractmethod",
    "Union",
    "Literal",
    "Optional",
    "Callable",
    "Dict",
    "List",
    "Tuple",
    "Set",
    "TypedDict",
    "TypeAlias",
    "AnyStr",
    "Path",
    "Deque",
    "Any",
    "TypeGuard",
    "TYPE_CHECKING",
    "Sequence",
    "namedtuple",
    "OrderedDict",
    "overload",
    "TypeVar",
    "NamedTuple",
    "PathType",
    "Iterable",
    "Iterator",
    "PathLike",
    "Number",
    "Type",
    "T",
    "get_overloads",
    "get_type_hints",
]

from abc import ABC, abstractmethod

from typing import (
    Any,
    Union,
    Optional,
    Literal,
    Callable,
    NamedTuple,
    Iterable,
    Iterator,
    Dict,
    List,
    Tuple,
    Type,
    Set,
    Deque,
    TypedDict,
    TypeAlias,
    TypeGuard,
    TYPE_CHECKING,
    Sequence,
    TypeVar,
    overload,
    get_overloads,
    get_type_hints,
)
from numbers import Number
from collections import namedtuple, OrderedDict
from pathlib import Path
from os import PathLike

T = TypeVar("T")  # Any type.
PathType: TypeAlias = Union[PathLike, str, bytes]
AnyStr: TypeAlias = Union[bytes, str]
