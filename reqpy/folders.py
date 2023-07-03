import logging
from pydantic import BaseModel, validator
from pathlib import Path
from typing import List
import shutil
from reqpy.__settings import RequirementFileSettings
from reqpy.__logging import printConsole
from reqpy.requirements import Requirement


# logger for logging
logger = logging.getLogger(__name__)


class FolderStructure(BaseModel):
    """Represents a folder structure.

    Attributes:
        main_folder (Path): The main folder path.
        requirements_folder (Path): The requirements folder path.
        definition_folder (Path): The definition folder path.
        annex_folder (Path): The annex folder path.
        reference_folder (Path): The reference folder path.
        image_folder (Path): The image folder path.

    """

    main_folder: Path
    requirements_folder: Path
    definition_folder: Path
    annex_folder: Path
    reference_folder: Path
    image_folder: Path

    class Config:
        """Configuration class for the FolderStructure class.

        Attributes:
            allow_mutation (bool): Whether mutation is allowed for
            the class FolderStructure.
            validate_assignment (bool): Whether to activate validation
            for assignment.
            extra (str): How to handle unknown fields.

        """

        allow_mutation = False
        validate_assignment = True
        extra = 'forbid'

    def __init__(self, currentFolderPath: Path = Path()):
        """Constructor for the FolderStructure class.

        Args:
            currentFolderPath (Path): The current folder path. Defaults to
              an empty Path object.

        """

        MAINFOLDERNAME = "requirements"

        # the main folder shall exist
        if not currentFolderPath.exists():
            raise FileExistsError(
                f"The folder {currentFolderPath} doesnt exist"
            )

        main_folder = currentFolderPath / MAINFOLDERNAME

        super().__init__(
            main_folder=main_folder,
            requirements_folder=main_folder / "Requirements",
            definition_folder=main_folder / "Definitions",
            annex_folder=main_folder / "Annex",
            reference_folder=main_folder / "References",
            image_folder=main_folder / "images",
        )

    @property
    def foldersList(self) -> List[Path]:
        """Get the list of folders.

        Returns:
            List[Path]: The list of folders.

        """
        return [info[1] for info in list(self)]

    def get_missing_folders(self) -> List[Path]:
        """Get the list of missing folders.

        Returns:
            List[Path]: The list of missing folders.

        """
        return [folder for folder in self.foldersList if not folder.exists()]

    def all_foders_exist(self) -> bool:
        """Check if all folders exist.

        Returns:
            bool: True if all folders exist, False otherwise.

        """
        if bool(self.get_missing_folders()):
            return False
        else:
            return True

    def create_folders(self) -> None:
        """Create all folders.

        """
        for folder in self.foldersList:
            folder.mkdir(parents=True, exist_ok=True)

            # log and console
            msg = f"create folder :{folder.absolute()}"
            logger.debug(msg)

            # add gitignore file
            FolderStructure.create_gitignore_file(folder)

    @staticmethod
    def create_gitignore_file(directory: Path) -> None:
        gitignore_path = Path(directory) / ".gitignore"
        gitignore_content = "# Add your gitignore rules here"

        # Create the .gitignore file
        gitignore_path.write_text(gitignore_content)

        # logging
        msg = (
            f"Created .gitignore file at: {gitignore_path.absolute()}")
        logger.debug(msg)

    def delete_folders(self) -> None:
        """Delete all folders.

        """
        shutil.rmtree(self.main_folder, ignore_errors=True)

        # logging
        msg = f"remove folder :{(self.main_folder).absolute()}\n"
        logger.debug(msg)

    def reset_folders(self) -> None:
        """Reset all folders by deleting and recreating them.

        """
        self.delete_folders()
        self.create_folders()
        # logging
        msg = f"reset folder :{(self.main_folder).absolute()}\n"
        logger.debug(msg)

    @staticmethod
    def validate_folders_structure(
            mainPath: Path,
            show_console: bool) -> bool:

        printConsole(
            message="Analysis of the REQPY folder structure",
            show_console=show_console,
            type="APPS")
        printConsole(
            message=f"Analyzed Path : {mainPath.absolute()}",
            show_console=show_console,
        )

        # check ùain folder existence
        printConsole(
            message="Check folder existence",
            show_console=show_console,
            type="ACTIVITY")
        if mainPath.exists() and mainPath.is_dir():
            printConsole(
                message="The main folder exist",
                show_console=show_console,
                type="OK"
            )
        else:
            printConsole(
                message="The main folder shall exist and be a directory",
                show_console=show_console,
                type="KO"
            )
            return False

        # check the folder structure
        printConsole(
            message="Check Reqpy Folders Structure",
            show_console=show_console,
            type="ACTIVITY"
        )

        folders = FolderStructure(mainPath)

        if folders.all_foders_exist():
            printConsole(
                message="All requested folders for reqpy exist ",
                show_console=show_console,
                type="OK"
            )
        else:
            missingFolders = folders.get_missing_folders()

            missingFolders = [str(path.absolute()) for path in missingFolders]
            missingFolders = "\n".join(missingFolders)
            message = f"The following folders are missing :\n {missingFolders}"

            printConsole(
                message=message,
                show_console=show_console,
                type="KO"
            )
            return False

        return True


class GenericFolder(BaseModel):
    folderPath: Path
    allowedExtensions: List[str]
    allowSubfolders: bool

    class Config:
        """Configuration class for the GenericFolder class.

        Attributes:
            allow_mutation (bool): Whether mutation is allowed for
            the class GenericFolder.
            validate_assignment (bool): Whether to activate validation
            for assignment.
            extra (str): How to handle unknown fields.

        """

        allow_mutation = False
        validate_assignment = True
        extra = 'forbid'

    @validator("folderPath")
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
                "folderPath property shall be an existing folder path\n" +
                f" - Current dir (relative): {str(folderPath)}\n" +
                f" - Current dir (absolute): {str(folderPath.absolute())}\n"
            )
        return folderPath

    def __init__(
            self,
            folderPath: Path,
            allowedExtensions: List[str],
            allowSubfolders: bool
                 ):
        super().__init__(
            folderPath=folderPath,
            allowedExtensions=allowedExtensions,
            allowSubfolders=allowSubfolders
            )

# ============================== GENERIC TOOLS ============================= #

    def has_appropriate_extension(self, file_path: Path) -> bool:
        """
        Check if a file has an appropriate extension based on a list of
          allowed extensions.

        Args:
            file_path (Path): The path to the file.

        Returns:
            bool: True if the file has an appropriate extension,
              False otherwise.
        """
        file_extension = file_path.suffix.lower()
        return file_extension in self.allowedExtensions

    def list_subdirectories(self) -> list[Path]:
        """
        List subdirectories of the directory as a list of Path objects.

        Args:
            None

        Returns:
            list[Path]: A list of Path objects representing the subdirectories.
        """
        subdirectories = [subdir for subdir in self.folderPath.iterdir()
                          if subdir.is_dir()]
        return subdirectories

    def list_all_files(self) -> list[Path]:
        """
        List all files in a directory and its subdirectories
        except .gitignore files

        Args:
            directory_path (Path): The path to the directory.

        Returns:
            list[Path]: A list of Path objects representing the files.
        """
        files = []
        for file_path in self.folderPath.glob('**/*'):
            if (file_path.is_file() and
               file_path.name != ".gitignore"):

                files.append(file_path)

        return files

    def list_invalid_files(self) -> list[Path]:
        """
        List files in the directory and its subdirectories that have invalid
          extensions.

        Args:
            None

        Returns:
            list[Path]: A list of Path objects representing the files with
              invalid extensions.
        """
        return [filePath for filePath in self.list_all_files()
                if not self.has_appropriate_extension(filePath)]

    def is_valid_folder_structure(self) -> bool:
        """
        Check if the folder structure is valid.

        Args:
            None

        Returns:
            bool: True if the folder structure is valid, False otherwise.
        """
        if (
             not self.list_subdirectories == [] and
             not self.allowSubfolders
           ):
            return False
        else:
            return True

    def is_all_files_has_valid_extension(self) -> bool:
        """
        Check if all files in the directory and its subdirectories have
          valid extensions.

        Args:
            None

        Returns:
            bool: True if all files have valid extensions, False otherwise.
        """
        if not self.list_invalid_files():
            return True
        else:
            return False

    def validate_Folder_Structure(
            self,
            show_console: bool) -> bool:

        # check subdirectories
        printConsole(
            message="Check subdirectories",
            show_console=show_console,
            type="ACTIVITY"
        )

        if self.is_valid_folder_structure():
            printConsole(
                message=" Folder structure is correct",
                show_console=show_console,
                type="OK"
            )
        else:
            msg = "The subdirectories are not permitted - Please remove it"
            printConsole(
                message=msg,
                show_console=show_console,
                type="KO"
            )
            return False

        # check file extensions
        printConsole(
            message="Check files extensions",
            show_console=show_console,
            type="ACTIVITY"
        )
        if self.is_all_files_has_valid_extension():
            printConsole(
                message=" all files extensions are correct",
                show_console=show_console,
                type="OK"
            )
        else:
            list_file = self.list_invalid_files()
            wrongFiles = [str(path.absolute()) for path in list_file]
            wrongFiles = "\n".join(wrongFiles)
            message = (
                "The following files has not conform"
                f" with the allowed extensions ie. {self.allowedExtensions}"
                f" :\n {wrongFiles}")
            printConsole(
                message=message,
                show_console=show_console,
                type="KO"
            )
            return False
        return True


class RequirementFolder(GenericFolder):
    def __init__(self, mainFolder: Path = Path()):

        # get the Reqpy folders structure
        foldersStructure = FolderStructure(mainFolder)

        super().__init__(
            folderPath=mainFolder / foldersStructure.requirements_folder,
            allowedExtensions=RequirementFileSettings.allowed_extensions,
            allowSubfolders=True)

    @staticmethod
    def validateFolder(
         mainPath: Path,
         show_console: bool
         ) -> bool:

        printConsole(
            message="Analysis of the Requirements files",
            show_console=show_console,
            type="APPS")

        reqFolderPath = FolderStructure(mainPath).requirements_folder

        printConsole(
            message=f"Analyzed Path : {reqFolderPath.absolute()}",
            show_console=show_console
        )

        # check main folder existence
        printConsole(
            message="Check folder existence",
            show_console=show_console,
            type="ACTIVITY")
        if reqFolderPath.exists() and reqFolderPath.is_dir():
            printConsole(
                message="The requirement folder exists",
                show_console=show_console,
                type="OK"
            )
        else:
            printConsole(
                message=("The requirement folder shall"
                         " exist and be a directory.\n"
                         f"The following path does not exist {reqFolderPath}"),
                show_console=show_console,
                type="KO"
            )
            return False

        reqFolder = RequirementFolder(
            mainFolder=mainPath
        )

        if not reqFolder.validate_Folder_Structure(show_console=show_console):
            return False

        # files statistic
        list_files = reqFolder.list_all_files()
        nb_files = len(list_files)

        printConsole(
            message=f"Number of detected files: {nb_files}",
            show_console=show_console,
            type="INFO"
        )

        # validation of requirements files
        printConsole(
            message="Analysis of the requirements files",
            show_console=show_console,
            type="ACTIVITY"
        )

        nb_errors = 0
        nb_fileNameError = 0
        idx = 0

        for file in list_files:
            idx += 1
            # get the relative filename for logging
            filename = str(file.relative_to(reqFolderPath))

            if Requirement.is_RequirementFile(file):
                printConsole(
                    message=(
                        f"[{idx:04d}/{nb_files}] " +
                        filename + "... OK"),
                    show_console=show_console,
                    type="OK"
                )

                if not Requirement.is_valid_RequirementFile_Name(file):
                    nb_fileNameError += 1
                    correctName = Requirement.read(file).get_valid_fileName()
                    currentName = file.name
                    printConsole(
                        message=(
                         "Please change filename to align with title.\n"
                         f"Correct Name : {correctName}\n"
                         f"Current Name : {currentName}"
                        ),
                        show_console=show_console,
                    )
            else:
                listError = Requirement.get_file_Errors(file)
                nb_errors += 1

                msg = (
                    f"{filename} ... KO with the following errors:\n" +
                    "\n".join(listError)
                    )
                printConsole(
                    message=msg,
                    show_console=show_console,
                    type="KO"
                )

        if nb_errors > 0:
            printConsole(
                message=f"{nb_errors} files with detected errors",
                show_console=show_console,
                type="KO"
            )
        if nb_fileNameError > 0:
            printConsole(
                message=f"{nb_fileNameError} files with inapropriate name",
                show_console=show_console,
                type="INFO"
            )
        return (nb_errors == 0 and nb_fileNameError == 0)
