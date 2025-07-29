import logging
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import ParamSpec, TypeVar

import attrs
import cattr

from apb.types import Pathish
from apb.vendor.strenum import StrEnum

# Create a default converter for serialization/deserialization using cattrs (for details
# on cattrs, see https://catt.rs/en/stable/). If we expand more into designing
# dataclasses that are round-trip serializable, e.g. `FeatureRecipe` in
# apb/workflow/create_collection.py, we should create a serialize subpackage modelled
# after or identical to this:
# https://github.com/ekiefl/pooltool/tree/main/pooltool/serialize
converter = cattr.Converter()
converter.register_unstructure_hook(StrEnum, lambda v: v.value)


def is_executable(program: str) -> bool:
    """Check if a program name is accessible."""
    return shutil.which(program) is not None


P = ParamSpec("P")
T = TypeVar("T")


def require_dependency(program: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator that checks if an external dependency is available before executing the function.

    Args:
        program: The name of the program dependency to check.

    Returns:
        A decorator function that will check for the dependency before executing the
        decorated function.

    Raises:
        RuntimeError: If the program is not available in PATH.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if not is_executable(program):
                raise RuntimeError(
                    f"Calling `{func.__name__}` requires external dependency '{program}', "
                    f"which is not found in PATH. Install {program} and ensure "
                    f"it's available in PATH."
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def run_command(command: list[str], log_stdout: bool = False) -> subprocess.CompletedProcess:
    """Runs a command using subprocess.

    Args:
        quiet:
            If True, stdout is not logged, otherwise it is. The stdout is not streamed,
            so no logging info until the subprocess completes.
    """

    if not len(command):
        raise ValueError("Empty command")

    if not is_executable(command[0]):
        command_string = " ".join(command)
        raise ValueError(f"'{command[0]}' from command '{command_string}' is not a program")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{result.stderr}")

    if log_stdout:
        logging.info(result.stdout)

    return result


@contextmanager
def maybe_temp_directory(
    existing_dir: Pathish | None = None,
) -> Generator[Path, None, None]:
    """Context manager that provides a temporary directory if an existing directory isn't passed.

    This context manager behaves like `tempfile.TemporaryDirectory` whenever
    `existing_dir` is None. Otherwise, it simply yields `existing_dir` after casting it
    as a pathlib.Path object.

    Args:
        existing_dir:
            An existing directory. If None (default), a new temporary
            directory is created.

    Yields:
        Path: The directory path.
    """
    if existing_dir is None:
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    else:
        yield Path(existing_dir)


@attrs.define
class Timer:
    # Initialized
    msg: str = attrs.field(default="elapsed time")
    quiet: bool = attrs.field(default=False)
    suffix: bool = attrs.field(default=True)

    # Internal
    start: datetime = attrs.field(default=None, init=False)
    end: datetime = attrs.field(default=None, init=False)
    time: timedelta = attrs.field(default=None, init=False)

    def __enter__(self):
        self.start = datetime.now()
        return self

    def __exit__(self, *_):
        self.end = datetime.now()
        self.time = self.end - self.start

        if self.quiet:
            return

        if self.suffix:
            print(f"{self.time} {self.msg.strip()}")
        else:
            print(f"{self.msg.strip()} {self.time}")
