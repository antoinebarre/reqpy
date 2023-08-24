"""DataBase management of REQPY"""

from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, field_validator
from pathlib import Path
from typing import List
from shutil import copy
from loguru import logger as log
from .constants import DEFAULT_REQPY_FILE_EXTENSION

from .exception import ReqpyDBException
from .tools.paths import Directory
from .tools.status import CheckStatus, CheckStatusList
from .__logging import Myconsole


class GenericDB(BaseModel):

    # ------------------------------ MODEL ----------------------------- #
    folderPath: Path
    allowSubfolders: bool
    allowAdditionalFiles: bool

    # ----------------------------- CONFIG ----------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # --------------------------- VALIDATION --------------------------- #
    @field_validator("folderPath")
    def folderPath_must_be_a_folder_existing_path(cls, folderPath: Path):
        """
        Validates that the folderPath attribute is an existing folder path.

        Args:
            cls: The class object.
            rootdir (Path): The root directory path to validate.

        Returns:
            Path: The validated root directory path.

        Raises:
            ValueError: If the rootdir attribute is not an
            existing folder path.
        """

        if not folderPath.is_dir():
            raise ValueError(
                f"folderPath property that defines {cls.__class__.__name__}" +
                " shall be an existing folder path\n" +
                f" - Current dir (relative): {str(folderPath)}\n" +
                f" - Current dir (absolute): {str(folderPath.absolute())}\n"
            )
        return folderPath

    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(
            self,
            folderPath: Path,
            allowSubfolders: bool,
            allowAdditionalFiles: bool,
                 ):
        super().__init__(
            folderPath=folderPath,
            allowSubfolders=allowSubfolders,
            allowAdditionalFiles=allowAdditionalFiles,
            )
    # --------------------------- VALIDATION TOOLS----------------------- #

    def validateDataBase(self) -> CheckStatusList:

        return CheckStatusList(
            [
                self.__validateSubFolder(),
                self.__validateAdditionalFiles(),
            ]
        )

    def __validateSubFolder(self) -> CheckStatus:
        checkName = "Validate Subfolders Existence"
        print("tata:")
        print(Directory(self.folderPath).list_subdirectories())

        if (Directory(self.folderPath).list_subdirectories() != [] and
                not self.allowSubfolders):

            return CheckStatus(
                check=checkName,
                valid=False,
                message=(
                    "No subfolder is permietted"
                    f" in the folder {self.folderPath.absolute()}"
                    )
            )
        else:
            return CheckStatus.createValid(checkName)

    def __validateAdditionalFiles(self) -> CheckStatus:
        checkName = "Validate Additional files existences"

        if (Directory(self.folderPath).list_invalid_files(
                validExtension=DEFAULT_REQPY_FILE_EXTENSION
                ) != [] and
                not self.allowAdditionalFiles):
            return CheckStatus(
                check=checkName,
                valid=False,
                message=(
                    "No additional file is permietted"
                    f" in the folder {self.folderPath.absolute()}")
            )
        else:
            return CheckStatus.createValid(checkName)

    # --------------------------- EXPORT TOOL -------------------------- #

    def __copy_folders_structure(
            self,
            destinationDir: Path,
            show_console: bool = False,
            ) -> None:
        try:
            Myconsole.apps(
                msg=f"Copy of the folder structure to {destinationDir}",
                show_console=show_console,
                )

            # target info :
            msg = f"Targeted Folder:{str(destinationDir.absolute())}"
            Myconsole.info(
                msg=msg,
                show_console=show_console,
            )

            # copy directories
            listdirs = Directory(dirPath=self.folderPath).list_subdirectories()

            for dirPath in listdirs:
                # get the new foldername
                folderName = str(dirPath.relative_to(self.folderPath))
                newDir = destinationDir / folderName

                # crate dir
                dirPath.mkdir(parents=True, exist_ok=True)

                # logging
                msg = f"Copy of the folder {newDir} OK"
                Myconsole.info(
                    msg=msg,
                    show_console=show_console,
                    )

        except Exception as e:
            msg = (
                "Impossible to copy the folders" +
                f" to {destinationDir}\n:" +
                str(e)
            )
            raise ReqpyDBException(msg)

    def __copy_additional_files(
            self,
            destinationDir: Path,
            show_console: bool = False,
    ) -> None:

        # Copy of the file
        try:
            Myconsole.apps(
                msg=f"Copy of the additional files to {destinationDir}",
                show_console=show_console,
            )

            # target info :
            msg = f"Targeted Folder:{str(destinationDir.absolute())}"
            Myconsole.info(
                msg=msg,
                show_console=show_console,
            )

            otherFiles = Directory(self.folderPath).list_invalid_files(
                validExtension=DEFAULT_REQPY_FILE_EXTENSION
            )

            # information about the number of additional files
            infoList = [str(fileName.absolute()) for fileName in otherFiles]
            log.trace(
                f"List of Files to copy :\n {infoList}")

            message = (
                f"Number of additional files to copy: {len(otherFiles)}"
            )
            Myconsole.info(
                msg=message,
                show_console=show_console,
            )

            if len(otherFiles) > 0:
                # initiate outputs
                newFiles = []

                # create progress bar
                sequence = Myconsole.progressBar(
                    sequence=otherFiles,
                    description="Copy of Additional Files...",
                    show_console=show_console,
                )

                for otherFile in sequence:
                    newFolder = (destinationDir /
                                 otherFile.relative_to(self.folderPath).parent)
                    newFile = newFolder / otherFile.name

                    # create destination folder if necessary
                    newFolder.mkdir(parents=True, exist_ok=True)

                    # copy file
                    copy(otherFile, newFile)

                    # add to list of new files path
                    newFiles.append(newFile)

                    # logging
                    msg = f"Copy to the file {newFile} OK"
                    Myconsole.info(
                        msg=msg,
                        show_console=show_console,
                    )

        except Exception as e:
            message = (
                "Impossible to copy the folders" +
                f" to {destinationDir}\n:" +
                str(e)
                )
            raise ReqpyDBException(message)

    def copyFoldersFiles(
            self,
            destinationDir: Path,
            show_console: bool = False,
            ) -> None:

        # create destination folder
        destinationDir.mkdir(parents=True, exist_ok=True)

        # validate folder structure
        if not self.validateDataBase().is_valid():
            msg = (
                f"The directory {self.folderPath} is not valid.\n"
                f"Detected Errors :\n{self.validateDataBase().tostr()}"
                )
            Myconsole.error(
                msg=msg,
                show_console=show_console
            )
            raise ReqpyDBException(msg)

        if self.allowAdditionalFiles:
            self.__copy_additional_files(
                destinationDir=destinationDir,
                show_console=show_console,
            )
        if self.allowSubfolders:
            self.__copy_folders_structure(
                destinationDir=destinationDir,
                show_console=show_console,
            )

