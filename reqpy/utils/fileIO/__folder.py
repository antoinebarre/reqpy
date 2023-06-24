"""Tools used for folder management and handling"""

import pathlib
from typing import List
__all__ = [
    "count_folders",
    "list_folders",
]


def list_folders(
        folder_path: pathlib.Path,
        include_subfolders: bool = False,
        exclude_dunder_folders: bool = False,
        exclude_hidden_folders: bool = False
) -> List[pathlib.Path]:
    """
    List the containing folders in a given folder.

    Args:
        folder_path: The path to the folder.
        include_subfolders: Whether to include subfolders in the listing
          (default: False).
        exclude_dunder_folders: Whether to exclude folders starting and ending
          with '__' (default: False).
        exclude_hidden_folders: Whether to exclude hidden folders starting
          with '.' (default: False).

    Returns:
        A list of pathlib.Path objects representing the containing folders.

    """

    def should_include_folder(folder_name: str) -> bool:
        if exclude_dunder_folders and folder_name.startswith("__") \
                and folder_name.endswith("__"):
            return False
        if exclude_hidden_folders and folder_name.startswith("."):
            return False
        return True

    containing_folders = []

    for item in folder_path.iterdir():
        if item.is_dir():
            if should_include_folder(item.name):
                containing_folders.append(item)
            if include_subfolders:
                containing_folders.extend(list_folders(
                    item,
                    include_subfolders=include_subfolders,
                    exclude_dunder_folders=exclude_dunder_folders,
                    exclude_hidden_folders=exclude_hidden_folders
                ))

    return containing_folders


def count_folders(
        folder_path: pathlib.Path,
        include_subfolders: bool = False,
        exclude_dunder_folders: bool = False,
        exclude_hidden_folders: bool = False
) -> int:
    """
    Count the number of folders in a given folder.

    Args:
        folder_path: The path to the folder.
        include_subfolders: Whether to include subfolders in the count
          (default: False).
        exclude_dunder_folders: Whether to exclude folders starting and ending
          with '__' (default: False).
        exclude_hidden_folders: Whether to exclude hidden folders starting
          with '.' (default: False).

    Returns:
        The number of folders.

    """

    def should_include_folder(folder_name: str) -> bool:
        if (exclude_dunder_folders and
           folder_name.startswith("__") and
           folder_name.endswith("__")):
            return False
        if exclude_hidden_folders and folder_name.startswith("."):
            return False
        return True

    folder_count = 0

    for item in folder_path.iterdir():
        if item.is_dir():
            if should_include_folder(item.name):
                folder_count += 1
            if include_subfolders:
                folder_count += count_folders(
                    item,
                    include_subfolders=include_subfolders,
                    exclude_dunder_folders=exclude_dunder_folders,
                    exclude_hidden_folders=exclude_hidden_folders
                )

    return folder_count
