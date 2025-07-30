import gc
import os
import ctypes
import psutil
import traceback
import platform
import subprocess
from .common import *
import importlib.util
from uuid import uuid4
from datetime import datetime
from functools import lru_cache, wraps


def default(entry: Any, other: Any):
    return entry if entry is not None else other


def log_traceback(
    exception: Exception,
    title: Optional[str] = None,
    limit: Optional[int] = None,
    invert_traceback: bool = False,
    limit_direction: Literal["from_end", "from_start"] = "from_end",
):
    """
    The function `print_traceback` prints the traceback information of an exception
    with optional title, limit, and inversion settings.
    """
    # except Exception as e:
    tb_lines = traceback.format_exception(
        type(exception), exception, exception.__traceback__, limit=limit
    )
    print()
    print("\n===========================")
    if isinstance(title, str) and title.strip():
        print(f"-----[ {title} ]-----")
    print(f"{exception}")
    print("-------[ Traceback ]-------")

    if invert_traceback:
        tb_lines.reverse()

    if isinstance(limit, int) and limit > 0:
        tb_lines = (
            tb_lines[-limit:] if limit_direction == "from_end" else tb_lines[:limit]
        )

    print("\n".join(tb_lines))
    print("===========================")


def get_os_info() -> Dict[str, str]:
    """Returns information about the operating system."""
    return {
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


def get_system_memory() -> Dict[str, Number]:
    """Returns system memory stats in bytes."""
    vm = psutil.virtual_memory()
    return {
        "total": vm.total,
        "available": vm.available,
        "used": vm.used,
        "free": vm.free,
        "percent": vm.percent,
    }


def get_pid_by_name(process_name: str, strict: bool = False) -> List[Dict[str, Any]]:
    if not strict:
        process_name = process_name.lower()
    results: List[Dict[str, Any]] = []
    for proc in psutil.process_iter():
        process_info = proc.as_dict(attrs=["pid", "name", "status", "ppid"])
        valid = (
            (process_name == process_info["name"])
            if strict
            else (process_name in process_info["name"].lower())
        )
        if valid:
            results.append(process_info)
    return results


def get_process_memory(pid: int = None) -> Dict[str, Any]:
    """Returns memory usage of a given process (or current one)."""
    pid = pid or os.getpid()
    proc = psutil.Process(pid)
    mem_info = proc.memory_info()
    return {
        "rss": mem_info.rss,  # Resident Set Size
        "vms": mem_info.vms,  # Virtual Memory Size
        "shared": getattr(mem_info, "shared", 0),
        "text": getattr(mem_info, "text", 0),
        "lib": getattr(mem_info, "lib", 0),
        "data": getattr(mem_info, "data", 0),
        "dirty": getattr(mem_info, "dirty", 0),
    }


def close_process_by_id(pid: int):
    """Example: `close_process("notepad.exe")`"""
    proc = psutil.Process(pid)
    process_info = proc.as_dict(attrs=["pid", "name", "status", "ppid"])
    try:
        proc.terminate()
        process_info["results"] = {"stats": "success", "reason": None}
        process_info["status"] = "terminated"

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        # Prudently handling potential exceptions arising during process information retrieval
        process_info["results"] = {"stats": "fail_safe", "reason": str(e)}
        pass

    except Exception as e:
        process_info["results"] = {"stats": "fail", "reason": str(e)}

    return process_info


def close_process_by_name(process_name: str, strict: bool = False):
    """Example: `close_process_by_name("notepad.exe")`"""
    if not strict:
        process_name = process_name.lower()
    results: List[Dict[str, Any]] = []

    for proc in psutil.process_iter():
        process_info = proc.as_dict(attrs=["pid", "name", "status", "ppid"])
        if not strict:
            valid = process_name in process_info["name"].lower()
        else:
            valid = process_info["name"] == process_name
        if not valid:
            continue
        try:
            proc.terminate()
            process_info["results"] = {"stats": "success", "reason": None}
            process_info["status"] = "terminated"
            print(f"Instance deletion successful: {process_info}")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            process_info["results"] = {"stats": "fail_safe", "reason": str(e)}

        except Exception as e:
            print(e)
            process_info["results"] = {"stats": "fail", "reason": str(e)}
        finally:
            results.append(process_info)

    return results


def clear_all_caches(registered_funcs: Optional[list] = None):
    """Clears global caches like lru_cache and runs garbage collection."""
    gc.collect()
    if registered_funcs:
        for func in registered_funcs:
            try:
                func.cache_clear()
            except AttributeError:
                pass


def malloc_trim():
    """On Linux, frees memory from malloc() back to the OS."""
    if platform.system() == "Linux":
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)


def clean_memory(clears: Optional[list] = None):
    """Performs full memory cleanup: gc, cache clears, and malloc_trim (Linux)."""
    clear_all_caches(clears)
    malloc_trim()


def terminal(
    *commant_lines: str,
    encoding: Optional[
        Union[
            Literal[
                "ascii",
                "utf-8",
                "iso-8859-1",
                "unicode-escape",
            ],
            str,
        ]
    ] = None,
    errors: Literal[
        "ignore",
        "strict",
        "replace",
        "backslashreplace",
        "surrogateescape",
    ] = "strict",
):
    """Terminal that returns the output
    made mostly to just to save a line of code."""
    return subprocess.run(
        commant_lines,
        shell=True,
        capture_output=True,
        text=True,
        encoding=encoding,
        errors=errors,
    ).stdout


def cache_wrapper(func):
    """
    A decorator to cache the function result while keeping the original documentation, variable names, etc.

    Example
        ```py
        @cache_wrapper
        def your_function(arg1:int, arg2:int) -> bool:
            \"\"\"
            compares if the first number is larger than the second number.
            args:
                arg1(int): The number that is expected to be larger than arg2.
                arg2(int): The number expected to be smaller than arg1

            return:
                bool: True if arg1 is larger than arg2 otherwise False.
            \"\"\"
            return arg1 > arg2
        ```
    """
    cached_func = lru_cache(maxsize=None)(func)

    # Apply the wraps decorator to copy the metadata from the original function
    @wraps(func)
    def wrapper(*args, **kwargs):
        return cached_func(*args, **kwargs)

    return wrapper


def get_encoding_aliases(entry: Optional[str] = None):
    from encodings.aliases import aliases

    if entry is None:
        return [(k, v) for k, v in aliases.items()]
    return [(k, v) for k, v in aliases.items() if entry in k or entry in v]


def get_unicode_chars(start_hex, end_hex):
    """
    # Example:
    my_character_set = get_unicode_chars('0E00', '0E7F')
    print("".join(my_character_set))
    """
    return [chr(code) for code in range(int(start_hex, 16), int(end_hex, 16) + 1)]


def import_functions(
    path: Union[str, Path],
    target_function: str,
    pattern: str = "*.py",
    scan_type: Literal["glob", "rglob"] = "rglob",
):
    """
    Imports and returns all functions from .py files in the specified directory matching a certain function name.

    Args:
        path (str or Path): The path of the directories to search for the Python files.
        target_function (str): The exact string representing the function name to be searched within each file.
        pattern (str, optional): Pattern of the file to be scanned. Defaults to "*.py" with covers all files with .py extension.
        scan_type (Literal["glob", "rglob"], optional): uses either glob or rglob to scan for the files within the directory. 'rglob' does a deeper scan, into the directory and sub-directory, while 'glob' will do the scan on the directory only.

    Returns:
        list: A list containing all the functions with the given name found in the specified directory and subdirectories.

    Example:
        >>> import_functions('/path/to/directory', 'some_function')
        [<function some_function at 0x7f036b4c6958>, <function some_function at 0x7f036b4c69a0>]
    """
    results = []
    if not Path(path).exists():
        return results
    if Path(path).is_dir():
        if scan_type == "rglob":
            python_files = [x for x in Path(path).rglob(pattern) if x.is_file()]
        else:
            python_files = [x for x in Path(path).glob(pattern) if x.is_file()]
    else:
        python_files = [path]
    for file in python_files:
        spec = importlib.util.spec_from_file_location(file.name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, target_function):
            results.append(getattr(module, target_function))
    return results


def get_current_time():
    """
    Returns the current date and time in a 'YYYY-MM-DD-HHMMSS' format.

    Returns:
        str: The current date and time.
    """
    return f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"


def get_random_name(source: Literal["time", "uuid4", "uuid4-hex"] = "uuid4"):
    assert isinstance(
        source, str
    ), f'Invalid type "{type(source)}". A value for `source` needs to be a valid str'
    assert source.strip(), "Source cannot be empty!"
    source = source.lower().strip()
    assert source in [
        "time",
        "uuid4",
        "uuid-hex",
    ], f'No such source \'{source}\'. It needs to be either "time", "uuid4" or "uuid4-hex"'
    match source:
        case "time":
            return get_current_time()
        case "uuid4":
            return str(uuid4())
        case _:
            return uuid4().hex
