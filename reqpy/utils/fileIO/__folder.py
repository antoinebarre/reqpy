"""Tools used for folder management and handling"""

import pathlib
from typing import List
__all__ = [
    "list_folders",
    "list_files"
]


def list_files(
        folder_path: pathlib.Path,
        include_subfolders: bool = False,
        exclude_dunder_folders: bool = False,
        exclude_hidden_folders: bool = False
) -> list[pathlib.Path]:
    """
    Lists files in a folder as pathlib.Path objects based
      on the provided options.

    Args:
        folder_path: The path of the existing folder to search for files.
        include_subfolders: Whether to include files in subfolders
          (default: False).
        exclude_dunder_folders: Whether to exclude folders starting with '__'
          (default: False).
        exclude_hidden_folders: Whether to exclude hidden folders starting
          with '.' (default: False).

    Returns:
        A list of pathlib.Path objects representing the files in the folder.
    """

    if not folder_path.exists():
        raise FileExistsError(
            f"The folder path {folder_path} does not exist"
        )
    
    files_list = []

    for file_path in folder_path.glob("**/*" if include_subfolders else "*"):
        if file_path.is_file():
            if (exclude_dunder_folders and
               file_path.parent.name.startswith("__")):
                continue
            if (exclude_hidden_folders and
               file_path.parent.name.startswith(".")):
                continue
            files_list.append(file_path)

    return files_list


def list_folders(
        folder_path: pathlib.Path,
        include_subfolders: bool = False,
        exclude_dunder_folders: bool = False,
        exclude_hidden_folders: bool = False
) -> List[pathlib.Path]:
    """
    List the containing folders in a given folder.

    Args:
        folder_path: The path to the existing folder.
        include_subfolders: Whether to include subfolders in the listing
          (default: False).
        exclude_dunder_folders: Whether to exclude folders starting and ending
          with '__' (default: False).
        exclude_hidden_folders: Whether to exclude hidden folders starting
          with '.' (default: False).

    Returns:
        A list of pathlib.Path objects representing the containing folders.

    """

    if not folder_path.exists():
        raise FileExistsError(
            f"The folder path {folder_path} does not exist"
        )

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

