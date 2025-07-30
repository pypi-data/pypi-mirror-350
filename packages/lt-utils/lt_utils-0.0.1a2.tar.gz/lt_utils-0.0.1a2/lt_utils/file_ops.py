__all__ = [
    "path_to_str",
    "get_file_name",
    "FileScan",
    "check_repeated_functions",
    "generate_all_",
    "mkdir_safe",
    "resolve_safe",
    "is_symlink",
    "is_mount",
    "delete_safe",
    "copy_safe",
    "move_safe",
    "rename_safe",
    "get_file_size",
    "get_file_info",
    "is_same_file",
    "hash_file",
    "get_disk_usage",
    "load_json",
    "save_json",
    "load_text",
    "save_text",
    "load_yaml",
    "save_yaml",
]

from .common import *
import json
import yaml
import shutil
import hashlib
from .misc_utils import get_current_time, ff_list
from .type_utils import is_file, is_dir, is_path_valid, is_pathlike, is_str


def path_to_str(entry: PathLike):
    is_pathlike(entry, False, True)
    return str(entry).replace("\\", "/")


def get_file_name(entry: PathLike, keep_extension: bool = True):
    is_pathlike(entry, False, True)
    f_name = Path(entry).name
    if keep_extension or "." not in f_name:
        return f_name
    return f_name[: f_name.rfind(".")]


class FileScan:
    @staticmethod
    def _setup_path_patterns(
        patterns: Optional[Union[str, List[str]]],
    ):
        """Helper function to `dirs` and `files`"""
        if not isinstance(patterns, (str, bytes, list, tuple)) or not patterns:
            patterns = ["*"]
        elif is_str(patterns, False):
            patterns = [
                (
                    patterns
                    if isinstance(patterns, str)
                    else patterns.decode(errors="ignore")
                )
            ]
        return patterns

    @staticmethod
    def _paths(
        entry: Union[PathLike, list[PathLike]],
        eval_fn: Callable[[PathType], bool],
        pattern: Optional[str] = None,
    ):
        assert isinstance(entry, (PathType, tuple, list))
        if isinstance(entry, PathType):
            entry = [entry]
        entry = ff_list(entry, PathType)
        results = []
        if pattern is None:
            pattern = "*"
        for dir in entry:
            results.extend(
                [
                    path_to_str(path)
                    for path in Path(dir).rglob(pattern)
                    if eval_fn(path)
                ]
            )
        return sorted(results)

    @staticmethod
    def dirs(
        path: Union[PathLike, list[PathLike]],
        patterns: Optional[Union[str, List[str]]] = None,
    ) -> list[str]:
        """Usage examples:
        ```python
        from lt_utils.file_ops import FileScan

        all_my_folders_in_data = FileScan.dirs("./data/")
        # lets suppose that the objective is to find
        # folders that contains the name similar to "created_01-10-2025"
        # but you want all that contains that name with different data-time:
        my_format_videos = FileScan.dirs("./data", "created_*")
        # now if more than one pattern of name is desired
        my_html_audios_texts = FileScan.dirs("C:/program_files/", ["log_*_finished", "*generated"])
        ```
        """
        patterns = FileScan._setup_path_patterns(patterns)
        results = []
        for pattern in patterns:
            results.extend(FileScan._paths(path, pattern=pattern, eval_fn=is_dir))
        return sorted(results)

    @staticmethod
    def files(
        path: Union[PathLike, list[PathLike]],
        patterns: Optional[Union[str, List[str]]] = None,
    ) -> list[str]:
        """Usage examples:
        ```python
        from lt_utils.file_ops import FileScan

        all_my_files_in_data = FileScan.files("./data/")
        my_format_videos = FileScan.files("./files/videos", ".format")
        my_html_audios_texts = FileScan.files("C:/users/documents/musics/", ["*.html", "*.normalized.txt", "podcast_*_favorits.wav"])
        ```
        """
        patterns = FileScan._setup_path_patterns(patterns)
        results = []
        for pattern in patterns:
            results.extend(FileScan._paths(path, pattern=pattern, eval_fn=is_file))
        return sorted(results)


def check_repeated_functions(target_dir: PathType):
    """Helper for finding repeated functions in python directories."""
    files = FileScan.files(target_dir, "*.py")
    found_fn = []
    repeated_fn = []
    for file in files:
        f_data = load_text(file, default_value="")
        for line in f_data.splitlines():
            if not line.strip() or not line.startswith("def") or "(" not in line:
                continue
            c_line = line[3 : line.find("(")].strip()
            if c_line in found_fn:
                repeated_fn.append((c_line, file))
            else:
                found_fn.append(c_line)
    return repeated_fn, found_fn


def generate_all_(target_dir: PathType, print_directly: bool = False):
    """Helper to create "__all__" for modules.
    it checks if the function or class does not
    has a '_' trailing its name, and adds it to the pool.
    It returns the dictionary with that content,
    but additionally, it can also print the already formated
    content for fast copy and paste.
    """
    found_contents: Dict[str, List[str]] = {}
    files = FileScan.files(target_dir, "*.py")
    for file in files:
        f_data = load_text(file, default_value="")
        found_contents[file] = []
        for line in f_data.splitlines():
            if not line.strip() or not line.startswith(("def", "class")):
                continue
            if line.startswith("class"):
                c_line = line[5:].strip()
                if c_line.startswith("_"):
                    continue
                if "(" in c_line:
                    slice_distance = c_line.find("(")
                elif ":" in c_line:
                    slice_distance = c_line.find(":")
                else:
                    # invalid item
                    continue
                c_line = c_line[:slice_distance].strip()
            else:
                c_line = line[3 : line.find("(")].strip()

            if c_line.startswith("_"):
                continue
            found_contents[file].append(c_line)
        if not found_contents[file]:
            found_contents.pop(file, None)
        else:
            if print_directly:
                print(f"-----[ {file} ]-----")
                print("__all__ = [")
                for _elem in found_contents[file]:
                    print(f'"{_elem}",')
                print("]\n----------------------------")
    return found_contents

def read_text_and_copy(path: PathType, encoding: str = "utf-8", errors: Literal["ignore", "strict", "replace"] = "ignore"):
    is_file(path, True)
    text = Path(path).read_text()
    

def mkdir_safe(path: PathType, parents: bool = True, exist_ok: bool = True) -> Path:
    """Create a directory if it doesn't exist. Returns the created/resolved Path."""
    is_pathlike(path, True, True)
    path_obj = Path(path)
    if not path_obj.exists():
        path_obj.mkdir(parents=parents, exist_ok=exist_ok)
    elif not path_obj.is_dir():
        raise NotADirectoryError(f"{path} exists but is not a directory.")
    return path_obj


def resolve_safe(path: PathType, strict: bool = False) -> Path:
    """Safely resolve a path. If `strict=True`, raises if path doesn't exist."""
    is_pathlike(path, True, True)
    path_obj = Path(path)
    try:
        return path_obj.resolve(strict=strict)
    except FileNotFoundError:
        if strict:
            raise
        return path_obj.absolute()


def is_symlink(path: PathType, validate: bool = False) -> bool:
    is_pathlike(path, True, True)
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
