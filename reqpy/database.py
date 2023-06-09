from .__settings import FolderStructure
from pathlib import Path
from pydantic import BaseModel, Field, validator
import os
import shutil

__all__ = [
    "ReqFolder"
]

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
            ValueError: If the rootdir attribute is not an existing folder path.
        """

        if not(rootdir.exists() and rootdir.is_dir()):
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
        
        for folder in FolderStructure.folder_structure :
            tmpPath = self.rootdir / folder
            tmpPath.mkdir(parents=True, exist_ok=False)
            print("create:",self.rootdir / folder)
    # TODO : add log
    
    def clean_dirs(
        self,
        forced:bool = False):
        # delete requirement folder and contents
        for folder in FolderStructure.folder_structure :
            shutil.rmtree(self.rootdir / folder,ignore_errors=True)
            print("remove:",self.rootdir / folder)

