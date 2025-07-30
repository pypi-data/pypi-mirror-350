"""Utility functions to interact with the filesystem."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from datetime import date, datetime
import logging
import os
from pathlib import Path
import stat as st
import sys
from typing import Optional, TypeVar, Union

_logger = logging.getLogger(__name__)

MAX_FILE_NUM = 100

R = TypeVar("R")


def safe_write_to_file(func: Callable[[Path], R], initial_path: Path) -> tuple[R, Path]:
    """Handle PermissionError when writing to a file.

    Execute some function that writes to a file and if it's not possible
    to write due to a PermissionError (e.g. the user has opened the file
    in Windows so can't be appended to) try to write to a new file instead.

    Args:
        func: Function to execute, that takes in the destination file path.
        initial_path: The desired destination file path.

    Returns:
        A tuple of the result of the function and the actual path finally written to.
    """
    try:
        r = func(initial_path)
        return r, initial_path
    except PermissionError as error:
        if initial_path.exists():
            i = 1
            new_path = (
                initial_path.parent / f"{initial_path.stem}{i}{initial_path.suffix}"
            )
            while new_path.exists() and i < MAX_FILE_NUM:
                i += 1
                new_path = (
                    initial_path.parent / f"{initial_path.stem}{i}{initial_path.suffix}"
                )
            _logger.warning(
                f"Error whilst writing to path {initial_path},"
                f" will try {new_path}: {error}"
            )
            if new_path.exists():
                raise error
            r = func(new_path)
            return r, new_path
        else:
            raise error


def get_file_last_modification_date(
    path: Union[str, os.PathLike], stat: Optional[os.stat_result] = None
) -> date:
    """Get the last modification date of a file.

    If the `stat` object is provided, then the information will be extracted from
    this in preference to getting a new one from the filesystem. Note that there is
    no checking that the stat object is up-to-date or even corresponds to the same
    file as `path`, so care should be taken to pass through the correct object.

    Args:
        path: The path to the file.
        stat: An optional `stat_result` object for the file, as returned by
            `os.stat(path)`. This can be used to avoid making a new filesystem query.

    Returns:
        The last modification date of the file.
    """
    if stat is None:
        stat = os.stat(path)

    timestamp = stat.st_mtime
    return datetime.fromtimestamp(timestamp).date()


def get_file_creation_date(
    path: Union[str, os.PathLike], stat: Optional[os.stat_result] = None
) -> date:
    """Get the creation date of a file with consideration for different OSs.

    If the `stat` object is provided, then the information will be extracted from
    this in preference to getting a new one from the filesystem. Note that there is
    no checking that the stat object is up-to-date or even corresponds to the same
    file as `path`, so care should be taken to pass through the correct object.

    :::caution

    It is not possible to get the creation date of a file on Linux. This method
    will return the last modification date instead. This will impact filtering of
    files by date.

    :::

    Args:
        path: The path to the file.
        stat: An optional `stat_result` object for the file, as returned by
            `os.stat(path)`. This can be used to avoid making a new filesystem query.

    Returns:
        The creation date of the file.
    """
    if stat is None:
        stat = os.stat(path)

    if sys.platform == "win32":
        timestamp = stat.st_ctime
    elif sys.platform == "darwin":
        timestamp = stat.st_birthtime
    else:
        # We're probably on Linux. No easy way to get creation dates here,
        # so we'll settle for when its content was last modified.
        timestamp = stat.st_mtime

    return datetime.fromtimestamp(timestamp).date()


def get_file_size(
    path: Union[str, os.PathLike], stat: Optional[os.stat_result] = None
) -> int:
    """Get the size, in bytes, of a file on the filesystem.

    If the `stat` object is provided, then the information will be extracted from
    this in preference to getting a new one from the filesystem. Note that there is
    no checking that the stat object is up-to-date or even corresponds to the same
    file as `path`, so care should be taken to pass through the correct object.

    Args:
        path: The path to the file.
        stat: An optional `stat_result` object for the file, as returned by
            `os.stat(path)`. This can be used to avoid making a new filesystem query.

    Returns:
        The size of the file, in bytes.
    """
    if stat is None:
        stat = os.stat(path)

    return stat.st_size


def is_file(
    path: Union[str, os.PathLike, os.DirEntry], stat: Optional[os.stat_result] = None
) -> bool:
    """Determine if a path is a file or not.

    If the `stat` object is provided, then the information will be extracted from
    this in preference to getting a new one from the filesystem. Note that there is
    no checking that the stat object is up-to-date or even corresponds to the same
    file as `path`, so care should be taken to pass through the correct object.

    Args:
        path: The path to check. Can also be an os.DirEntry as from scandir() or
            scantree().
        stat: An optional `stat_result` object for the path, as returned by
            `os.stat(path)`. This can be used to avoid making a new filesystem query.

    Returns:
        The size of the file, in bytes.
    """
    path_or_entry: Union[Path, os.DirEntry]
    if not isinstance(path, os.DirEntry):
        path_or_entry = Path(path)
    else:
        path_or_entry = path

    # If `stat` isn't provided, then defer to built-in methods (which will make an
    # `os.stat()` call
    if stat is None:
        return path_or_entry.is_file()
    # Otherwise, determine it using the provided details
    # This is copied from genericpath.py
    else:
        return st.S_ISREG(stat.st_mode)


def scantree(root: Union[str, os.PathLike]) -> Iterator[os.DirEntry]:
    """Recursively iterate through a folder as in scandir(), yielding file entries."""
    with os.scandir(Path(root)) as it:
        for entry in it:
            # Recurse into subdirectories
            # follow_symlinks=False as per https://peps.python.org/pep-0471/#examples
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry
