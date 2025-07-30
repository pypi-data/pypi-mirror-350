from .common import *
import json
import yaml
import shutil
import hashlib
from .misc_utils import get_current_time
from .types_utils import is_file, is_dir, is_path_valid, is_pathlike, is_str


def check_path(
    path: PathType,
    path_type: Literal["file", "dir", "any"] = "any",
    validate: bool = False,
) -> TypeGuard[PathType]:
    assert path_type in {
        "file",
        "dir",
        "any",
    }, f'Invalid path_type "{path_type}". Must be "file", "dir" or "any".'
    if not is_path_valid(path, validate):
        return False

    if path_type == "any":
        return True
    return is_file(path, validate) if path_type == "file" else is_dir(path, validate)


def mkdir_safe(path: PathType, parents: bool = True, exist_ok: bool = True) -> Path:
    """Create a directory if it doesn't exist. Returns the created/resolved Path."""
    path_obj = Path(path)
    if not path_obj.exists():
        path_obj.mkdir(parents=parents, exist_ok=exist_ok)
    elif not path_obj.is_dir():
        raise NotADirectoryError(f"{path} exists but is not a directory.")
    return path_obj


def resolve_safe(path: PathType, strict: bool = False) -> Path:
    """Safely resolve a path. If `strict=True`, raises if path doesn't exist."""
    path_obj = Path(path)
    try:
        return path_obj.resolve(strict=strict)
    except FileNotFoundError:
        if strict:
            raise
        return path_obj.absolute()


def is_symlink(path: PathType, validate: bool = False) -> bool:
    if not is_path_valid(path, validate):
        return False
    result = Path(path).is_symlink()
    assert not validate or result
    return result


def is_mount(path: PathType, validate: bool = False) -> bool:
    if not is_path_valid(path, validate):
        return False
    result = Path(path).is_mount()
    assert not validate or result
    return result


def delete_safe(path: PathType, missing_ok: bool = True) -> bool:
    """Deletes a file or directory (recursively)."""
    if not is_path_valid(path, validate=not missing_ok):
        return False
    p = Path(path)
    if p.is_file() or p.is_symlink():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)
    return True


def copy_safe(src: PathType, dst: PathType, overwrite: bool = False) -> Path:
    """Copies a file from src to dst. Returns destination path."""
    if not is_file(src):
        raise FileNotFoundError(f"Source file not found: {src}")

    src_path = Path(src)
    dst_path = Path(dst)

    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {dst_path}")
    if dst_path.is_dir():
        dst_path = dst_path / src_path.name

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)
    return dst_path


def move_safe(src: PathType, dst: PathType, overwrite: bool = False) -> Path:
    """Moves src to dst (file or folder)."""
    if not is_path_valid(src):
        raise FileNotFoundError(f"Source path not valid: {src}")

    src_path = Path(src)
    dst_path = Path(dst)

    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {dst_path}")

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src_path), str(dst_path))
    return dst_path


def rename_safe(src: PathType, new_name: str) -> Path:
    """Renames a file or directory in-place."""
    if not is_path_valid(src):
        raise FileNotFoundError(f"Source path not valid: {src}")
    src_path = Path(src)
    target = src_path.with_name(new_name)
    if target.exists():
        raise FileExistsError(f"Target already exists: {target}")
    return src_path.rename(target)


def get_file_size(path: PathType, validate: bool = False) -> int:
    """Returns file size in bytes."""
    if not is_file(path, validate):
        return -1
    return Path(path).stat().st_size


def get_file_info(path: PathType, validate: bool = False) -> dict:
    """Returns a dictionary of common file metadata."""
    if not is_path_valid(path, validate):
        return {}

    p = Path(path)
    stat = p.stat()
    return {
        "size_bytes": stat.st_size,
        "last_modified": stat.st_mtime,
        "last_accessed": stat.st_atime,
        "created": stat.st_ctime,
        "is_symlink": p.is_symlink(),
        "is_file": p.is_file(),
        "is_dir": p.is_dir(),
        "absolute_path": str(p.resolve()),
        "name": p.name,
        "extension": p.suffix,
    }


def is_same_file(path1: PathType, path2: PathType, validate: bool = False) -> bool:
    """Checks if two paths refer to the same file (resolved absolute paths)."""
    if not (is_path_valid(path1, validate) and is_path_valid(path2, validate)):
        return False
    return Path(path1).resolve() == Path(path2).resolve()


def hash_file(
    path: PathType,
    algo: str = "sha256",
    chunk_size: int = 65536,
    validate: bool = False,
) -> str:
    """Returns a hexadecimal digest of a file using the given algorithm."""
    if not is_file(path, validate):
        return ""

    hasher = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_disk_usage(path: PathType = ".", validate: bool = False) -> dict:
    """Returns total, used, and free disk space in bytes."""
    if not is_pathlike(path, validate):
        return {}
    usage = shutil.disk_usage(str(path))
    return {"total": usage.total, "used": usage.used, "free": usage.free}


def which(command: str) -> str:
    """Returns the full path of a command (like Unix 'which')."""
    from shutil import which as _which

    return _which(command) or ""


def load_json(
    path: Union[str, Path],
    default: Optional[Any] = None,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
) -> Union[list, dict]:
    """
    Load JSON/JSONL data from a file.

    Args:
        path (Union[str, Path]): The path to the JSON file.

    Returns:
        Union[list, dict]: The loaded JSON data as a list, dictionary, or default if the path is not valid and default is not None.
    """
    is_pathlike(path, True, True)
    if not is_file(path, validate=default is None):
        return default
    path = Path(path)

    contents = path.read_text(encoding=encoding, errors=errors)
    if path.name.endswith(".jsonl"):
        results = []
        for line in contents.splitlines():
            try:
                results.append(json.loads(line))
            except:
                pass
        return results

    return json.loads(contents)


def save_json(
    path: Union[str, Path],
    content: Union[list, dict, tuple, map, str, bytes],
    indent: int = 4,
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    separators: tuple[str, str] | None = None,
    sort_keys: bool = False,
) -> None:
    """
    Save JSON data to a file.

    Args:
        path (Union[str, Path]): The path to save the JSON file.
        content (Union[list, dict]): The content to be saved as JSON.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".
        indent (int, optional): The indentation level in the saved JSON file. Defaults to 4.
    """
    is_pathlike(path, True, True)
    path = Path(path)
    if not path.name.endswith((".json", ".jsonl")):
        path = Path(path, f"{get_current_time()}.json")

    path.parent.mkdir(exist_ok=True, parents=True)

    dumps_kwargs = dict(
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        separators=separators,
        sort_keys=sort_keys,
    )
    if path.name.endswith(".jsonl"):
        if is_str(content):
            content = content.rstrip()
        else:
            content = json.dumps(content, **dumps_kwargs).rstrip()
    else:
        content = json.dumps(content, indent=indent, **dumps_kwargs)
    path.write_text(content, encoding=encoding, errors=errors)


def load_text(
    path: Union[Path, str],
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    default_value: Optional[Any] = None,
    **kwargs,
) -> str:
    is_pathlike(path, True, True)
    if not is_file(path, validate=default_value is None):
        return default_value
    return Path(path).read_text(encoding, errors=errors)


def save_text(
    path: Union[Path, str],
    content: str,
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    newline: Optional[str] = None,
) -> None:
    """Save a text file to the provided path.

    args:
        raises: (bool, optional): If False, it will not raise the exception when somehting goes wrong, instead it will just print the traceback.
    """
    is_pathlike(path, True, True)
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(content, encoding=encoding, errors=errors, newline=newline)


def load_yaml(
    path: Union[Path, str],
    default_value: Optional[Any] = None,
    safe_loader: bool = False,
) -> Optional[Union[List[Any], Dict[str, Any]]]:
    """
    Loads YAML content from a file.

    Args:
        path (Union[Path, str]): The path to the file.
        default_value (Any | None): If something goes wrong, this value will be returned instead.
        safe_loader (bool): If True, it will use the safe_load instead. Defaults to False

    Returns:
        Optional[Union[List[Any], Dict[str, Any]]]: The loaded YAML data.
    """
    is_pathlike(path, True, True)
    if not is_file(path, validate=default_value is None):
        return default_value
    loader = yaml.safe_load if safe_loader else yaml.unsafe_load
    return loader(Path(path).read_bytes())


def save_yaml(
    path: Union[Path, str],
    content: Union[List[Any], Tuple[Any, Any], Dict[Any, Any]],
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    safe_dump: bool = False,
) -> None:
    """Saves a YAML file to the provided path.

    Args:
        path (Union[Path, str]): The path where the file will be saved.
        content (Union[List[Any], Tuple[Any, Any], Dict[Any, Any]]): The data that will be written into the file.
        encoding (str, optional): The encoding of the output. Default is 'utf-8'. Defaults to "utf-8".
        safe_dump (bool, optional): If True, it uses the safe_dump method instead. Defaults to False.
    """
    is_pathlike(path, True, True)
    Path(path).parent.mkdir(exist_ok=True, parents=True)

    save_func = yaml.safe_dump if safe_dump else yaml.dump
    data = save_func(data=content, stream=None, encoding=encoding)
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        path.write_text(data, encoding=encoding, errors=errors)
