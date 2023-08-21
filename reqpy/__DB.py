"""DataBase management of REQPY"""

from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, field_validator
from pathlib import Path
from typing import List
import shutil
from loguru import logger as log

from reqpy.exception import ReqpyDBException
from reqpy.tools.paths import Directory
#from .__logging import Myconsole



# # generic error Status
# @dataclass
# class FileError:
#     filePath: Path
#     errorMsg: str



class GenericDB(BaseModel):

    # ------------------------------ MODEL ----------------------------- #
    folderPath: Directory
    allowSubfolders: bool
    allowAdditionalFiles: bool

    # ----------------------------- CONFIG ----------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # --------------------------- VALIDATION --------------------------- #

    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(
            self,
            folderPath: Path,
            allowSubfolders: bool,
            allowAdditionalFiles: bool,
                 ):
        super().__init__(
            folderPath=Directory(folderPath),
            allowSubfolders=allowSubfolders,
            allowAdditionalFiles=allowAdditionalFiles,
            )

# =========================== VALIDATION TOOLS ========================== #
    def is_valid_folder_structure(self) -> bool:
        """
        Check if the folder structure is valid.

        Args:
            None

        Returns:
            bool: True if the folder structure is valid, False otherwise.
        """
        if (
             not self.folderPath.list_subdirectories() == [] and
             not self.allowSubfolders
           ):
            return False
        else:
            return True

    def is_conform_to_file_rules(self) -> bool:
        if (
                not self.folderPath.list_invalid_files(
            validExtension=self.va
                ) == [] and
                not self.allowAdditionalFiles
                ):
            return False
        else:
            return True

    def get_Folder_Conformance_Status(
            self,
            show_console: bool) -> bool:

        # check subdirectories
        Myconsole.task(
            msg="Check subdirectories",
            show_console=show_console)

        if self.is_valid_folder_structure():
            message = "Folder structure is correct"
            Myconsole.ok(
                msg=message,
                show_console=show_console,
            )
            log.info(message)
        else:
            message = "The subdirectories are not permitted - Please remove it"
            Myconsole.ko(
                msg=message,
                show_console=show_console
            )
            log.error(message)
            return False

        # check file extensions
        Myconsole.task(
            msg="Check additional files",
            show_console=show_console,
            )
        if self.is_conform_to_file_rules():
            message = " all files are correct"
            Myconsole.ok(
                msg=message,
                show_console=show_console,
            )
            log.info(message)
        else:
            list_file = self.list_invalid_files()
            wrongFiles = [str(path.absolute()) for path in list_file]
            wrongFiles = "\n".join(wrongFiles)
            message = (
             "Additional files are not permitted"
             f". The list of allowed extensions is {self.allowedExtensions}\n"
             f"Detected inapropriate files :\n {wrongFiles}")
            Myconsole.ko(
                msg=message,
                show_console=show_console,
            )
            log.error(message)
            return False
        return True

    @log.catch
    def validate_Folder_Conformance_Status(
            self,
            show_console: bool = False,
            ) -> None:
        if not self.get_Folder_Conformance_Status(
                    show_console=show_console,
                    ):
            msg = (
                f"The folder {self.folderPath} is not well strucutured"
                "The allowed configuration is:\n"
                f"- allow subdirectories : {self.allowSubfolders}\n"
                f"- allow additional files: {self.allowAdditionalFiles}\n"
                f"- allow extensions : {self.allowedExtensions}"
                )
            raise reqpyDataBaseException(msg)

# ---------------------- GENERIC EXPORT TOOLS ---------------------- #
    @log.catch
    def copy_folders_structure(
            self,
            destinationDir: Path,
            show_console: bool = False,
            ) -> None:

        try:
            Myconsole.apps(
                msg=f"Copy of the folder structure to {destinationDir}",
                show_console=show_console,
                )
            # validate folder structure
            self.validate_Folder_Conformance_Status()

            # create destination folder
            destinationDir.mkdir(parents=True, exist_ok=True)

            # copy directories
            listdirs = self.list_subdirectories()

            for dirPath in listdirs:
                # get the new foldername
                folderName = str(dirPath.relative_to(self.folderPath))
                newDir = destinationDir / folderName

                # crate dir
                dirPath.mkdir(parents=True, exist_ok=True)

                # logging
                msg = f"Copy of the folder {newDir}"
                Myconsole.info(
                    msg=msg,
                    show_console=show_console,
                    )
                log.info(msg)

        except Exception as e:
            msg = (
                "Impossible to copy the folders" +
                f" to {destinationDir}\n:" +
                str(e)
            )
            raise reqpyDataBaseException(msg)

    @log.catch
    def copy_additional_files(
            self,
            destinationDir: Path,
            show_console: bool = False,
    ) -> None:

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
            log.trace(msg)
            # validate folder structure
            self.validate_Folder_Conformance_Status()

            # create destination folder
            destinationDir.mkdir(parents=True, exist_ok=True)

            otherFiles = self.list_invalid_files()

            # information about the number of additional files
            infoList = [str(fileName.absolute()) for fileName in otherFiles]
            log.trace(
                f"List of Files to copy :\n {infoList}")

            message = (
                f"Number of additional files to copy: {len(otherFiles)}"
            )
            log.trace(message)
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
                    shutil.copy(otherFile, newFile)

                    # add to list of new files path
                    newFiles.append(newFile)

                    message = f"Copy of the file {otherFile}"

                    log.trace(message)

        except Exception as e:
            message = (
                "Impossible to copy the folders" +
                f" to {destinationDir}\n:" +
                str(e)
            ),
            raise reqpyDataBaseException(message)
