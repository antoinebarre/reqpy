from .__settings import FolderStructure, RequirementFileSettings
from pathlib import Path
from pydantic import BaseModel, validator
import shutil
from typing import List

__all__ = [
    "ReqFolder"
]


class DataBaseError(Exception):
    # raised when there is a error in the database handling
    pass


class ReqFolder(BaseModel):
    """
    Represents a requirement folder.

    Attributes:
        rootdir (Path): The root directory path of the requirement folder.
    """

    rootdir: Path

    @validator("rootdir")
    def rootdir_must_be_a_folder_existing_path(cls, rootdir: Path):
        """
        Validates that the rootdir attribute is an existing folder path.

        Args:
            cls: The class object.
            rootdir (Path): The root directory path to validate.

        Returns:
            Path: The validated root directory path.

        Raises:
            ValueError: If the rootdir attribute is not an
            existing folder path.
        """

        if not (rootdir.exists() and rootdir.is_dir()):
            raise ValueError(
                "rootdir property shall be an existing folder path\n" +
                f" - Current dir (relative): {str(rootdir)}\n" +
                f" - Current dir (absolute): {str(rootdir.absolute())}\n"
            )
        return rootdir

    def create_dirs(self):
        """
        Creates the directories defined in the FolderStructure.

        Returns:
            None
        """

        for folder in FolderStructure.folder_structure:
            tmpPath = self.rootdir / folder
            tmpPath.mkdir(parents=True, exist_ok=True)
            print("create:", self.rootdir / folder)
    # TODO : add log

    def clean_dirs(self, forced: bool = True):
        """
        Delete the requirement folders and their contents.

        Args:
            forced (bool): If True, ignore errors and force deletion.
            Defaults to True.
        """
        for folder in FolderStructure.folder_structure:
            shutil.rmtree(self.rootdir / folder, ignore_errors=forced)
            print("remove:", self.rootdir / folder)

    def get_missing_drectories(self) -> List[Path]:
        """
        Validate if all required folders are present in the root path.

        Returns:
            List[Path]: A list of missing folders.
        """
        missing_folders: list[Path] = []

        for folder in FolderStructure.folder_structure:
            tested_Path = self.rootdir / folder

            if not tested_Path.exists():
                missing_folders.append(tested_Path)
        return missing_folders

    def get_list_of_files(self) -> list[Path]:
        """
        Get a list of files in the requirements folder.

        Returns:
            list[Path]: A list of Path objects representing files in the
            requirements folder.

        Raises:
            DataBaseError: If the required folders are missing.
        """
        # check if the folders are available
        if not self.is_correct_folders():
            msg = (
                "No requirements folders - " +
                "The following folders are missing:\n" +
                f"{self.get_missing_drectories}"
            )
            raise DataBaseError(msg)

        requirement_folder = self.rootdir / FolderStructure.main_folder

        p = requirement_folder.glob('**/*')
        return [x for x in p if x.is_file()]

    def get_incorrect_files(self) -> List[Path]:
        """
        Get a list of files in the requirements folder with incorrect
        extensions.

        Returns:
            List[Path]: A list of Path objects representing incorrect files.
        """
        # get the list of files
        list_files = self.get_list_of_files()

        return [
            file for file in list_files
            if file.suffix not in RequirementFileSettings.allowed_extensions
        ]

    def is_correct_files(self) -> bool:
        """
        Check if all files in the requirements folder have the correct
        extension.

        Returns:
            bool: True if all files have the correct extension, False
            otherwise.
        """
        if self.get_incorrect_files():  # incorrect files found
            return False
        else:
            return True

    def is_correct_folders(self) -> bool:
        """
        Check if all mandatory folders are present.

        Returns:
            bool: True if all mandatory folders are present, False otherwise.
        """
        if self.get_missing_drectories():  # missing data found
            return False
        else:  # no missing data
            return True
