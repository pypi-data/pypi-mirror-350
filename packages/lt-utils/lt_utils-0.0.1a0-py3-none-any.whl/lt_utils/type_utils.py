__all__ = [
    "is_pathlike",
    "is_path_valid",
    "is_file",
    "is_dir",
    "is_valid",
    "is_num",
    "is_array",
    "is_list",
    "is_dict",
    "is_tuple",
    "is_int",
    "is_float",
    "is_bool",
    "is_str",
    "is_seq",
    "is_sequence_of",
    "is_list_of",
    "is_dict_of",
    "is_tuple_of",
]

from .common import *

Array: TypeAlias = Union[list, tuple]

def is_pathlike(
    entry: Any, check_if_empty: bool = False, validate: bool = False
) -> TypeGuard[PathType]:
    begin = isinstance(entry, PathType)
    assert (
        not validate or begin
    ), f'"{entry}" is not a valid path-like. It is a {type(entry)} type'
    results = not check_if_empty or str(entry).strip()
    assert not validate or results, "The provided entry was an empty!"
    return results


def is_path_valid(path: PathLike, validate: bool = False) -> bool:
    if not is_pathlike(path, validate):
        return False
    result = Path(path).exists()
    assert not validate or result, f'The path "{path}" is not a valid path!'
    return result


def is_file(path: PathLike, validate: bool = False) -> bool:
    if not is_path_valid(path, validate):
        return False
    result = Path(path).is_file()
    assert not validate or result, f'The path "{path}" does not point to a valid file!'
    return result


def is_dir(path: PathLike, validate: bool = False) -> bool:
    if not is_path_valid(path, validate):
        return False
    result = Path(path).is_dir()
    assert (
        not validate or result
    ), f'The path "{path}" does not point to a valid directory!'
    return result


def is_valid(
    entry: Any,
    validate: bool = False,
) -> TypeGuard[T]:
    results = entry is not None
    assert not validate or results
    return results


def is_num(
    entry: Any,
    validate: bool = False,
) -> TypeGuard[Number]:
    results = isinstance(entry, Number)
    assert (
        results or not validate
    ), f"'{entry}' is not a valid number! It is type: {type(entry)}"
    return results


def is_array(
    entry: Any,
    check_if_empty: bool = True,
    validate: bool = False,
) -> TypeGuard[Array]:
    """The type `Array` itself does not exist in python, so, here
    we do check if the value is either a `List` or a `Tuple`, with
    both can be considered one.

    Note that Lists are mutable while Tuples aren't.
    If its needed certainty, then use `is_list` or `is_tuple` instead.
    """
    result = isinstance(entry, Array) and (not check_if_empty or bool(entry))
    assert not validate or result
    return result


def is_list(
    entry: Any,
    check_if_empty: bool = True,
    validate: bool = False,
) -> TypeGuard[list]:
    result = isinstance(entry, list) and (not check_if_empty or bool(entry))
    assert not validate or result
    return result


def is_dict(
    entry: Any,
    check_if_empty: bool = True,
    validate: bool = False,
) -> TypeGuard[dict]:
    result = isinstance(entry, dict) and (not check_if_empty or bool(entry))
    assert not validate or result
    return result


def is_tuple(
    entry: Any,
    check_if_empty: bool = True,
    validate: bool = False,
) -> TypeGuard[tuple]:
    result = isinstance(entry, tuple) and (not check_if_empty or bool(entry))
    assert not validate or result
    return result


def is_int(entry: Any, validate: bool = False) -> TypeGuard[int]:
    result = isinstance(entry, int) and not isinstance(
        entry, bool
    )  # Prevents `True` being treated as `1`
    assert not validate or result
    return result


def is_float(entry: Any, validate: bool = False) -> TypeGuard[float]:
    result = isinstance(entry, float)
    assert not validate or result
    return result


def is_bool(entry: Any, validate: bool = False) -> TypeGuard[bool]:
    result = isinstance(entry, bool)
    assert not validate or result
    return result


def is_str(
    entry: Any,
    strip_str: bool = True,
    check_if_empty: bool = True,
    validate: bool = False,
) -> TypeGuard[AnyStr]:
    """Check if an entry is a string or bytes."""
    first_check = isinstance(entry, AnyStr)
    if not first_check:
        assert (
            not validate
        ), f'"{entry}" is not a valid string, it is a type: {type(entry)}'
        return False
    results = not check_if_empty or bool(entry.strip() if strip_str else entry)
    assert not validate or results, "The provided string was a empty string!"
    return results


def is_seq(
    entry: Any,
    check_if_empty: bool = True,
    validate: bool = False,
    allow_str: bool = False,
) -> TypeGuard[Sequence]:
    """
    Check if entry is a non-string sequence (optional empty check).

    Args:
        check_if_empty: If True, requires the sequence to be non-empty.
        allow_str: If False, str/bytes will not be considered valid sequences.
    """
    begin = isinstance(entry, AnyStr)
    if not allow_str and begin:
        assert not validate
        return begin

    result = isinstance(entry, Sequence) and (
        allow_str or not isinstance(entry, AnyStr)
    )
    assert not validate or result
    if result and check_if_empty:
        result = bool(entry)
        assert not validate or result
    return result


def is_sequence_of(item_type: Type, entry: Any, validate: bool = False):
    """
    Check if entry is a sequence and all elements are of the given item_type.

    Args:
        item_type: The expected type of each element.
        entry: The object to check.
        validate: If True, raises AssertionError when check fails.

    Returns:
        True if valid, False otherwise.
    """
    results = is_array(entry, False, False) and all(
        isinstance(i, item_type) for i in entry
    )
    assert not validate or results
    return results


def is_list_of(item_type: Type, entry: Any, validate: bool = False) -> bool:
    """Return True if items is a list and all elements are of the given item_type."""
    return isinstance(entry, list) and is_sequence_of(item_type, entry, validate)


def is_dict_of(
    key_type: Type, value_type: Type, entry: Any, validate: bool = False
) -> bool:
    """Return True if d is a dict and all keys/values match the given types."""
    results = (
        isinstance(entry, dict)
        and all(isinstance(k, key_type) for k in entry.keys())
        and all(isinstance(v, value_type) for v in entry.values())
    )
    assert not validate or results
    return results


def is_tuple_of(types: tuple, entry: Any, validate: bool = False) -> bool:
    """Check if an object is a tuple of specific types."""
    return isinstance(entry, tuple) and is_sequence_of(types, entry, validate)
