from pydantic import BaseModel
from pathlib import Path
from typing import List
import shutil
from .__logging import Myconsole
from loguru import logger as log


# Default Values :
DEFAULT_EXPORT_DIR_NAME = "report"


# Default Settings
IGNORE_FILE_LIST = [
    ".gitignore",
]


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
    introduction_folder: Path

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
            introduction_folder=main_folder / "Introduction"
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
            log.debug(msg)

            # add gitignore file
            FolderStructure.create_gitignore_file(folder)

    @property
    def default_export_directory(self) -> Path:
        return self.main_folder / DEFAULT_EXPORT_DIR_NAME

    @log.catch
    @staticmethod
    def create_gitignore_file(directory: Path) -> None:
        gitignore_path = Path(directory) / ".gitignore"
        gitignore_content = "# Add your gitignore rules here"

        # Create the .gitignore file
        gitignore_path.write_text(gitignore_content)

        # logging
        msg = (
            f"Created .gitignore file at: {gitignore_path.absolute()}")
        log.debug(msg)

    @log.catch
    def delete_folders(self) -> None:
        """Delete all folders.

        """
        shutil.rmtree(self.main_folder, ignore_errors=True)

        # logging
        msg = f"remove folder :{(self.main_folder).absolute()}\n"
        log.debug(msg)

    @log.catch
    def reset_folders(self) -> None:
        """Reset all folders by deleting and recreating them.

        """
        self.delete_folders()
        self.create_folders()
        # logging
        msg = f"reset folder :{(self.main_folder).absolute()}\n"
        log.debug(msg)

    @staticmethod
    def validate_folders_structure(
            mainPath: Path,
            show_console: bool) -> bool:

        Myconsole.task(
            msg="Analysis of the REQPY folder structure",
            show_console=show_console,
            )
        Myconsole.info(
            msg=f"Analyzed Path : {mainPath.absolute()}",
            show_console=show_console,
        )

        # check ùain folder existence
        Myconsole.task(
            msg="Check folder existence",
            show_console=show_console,
            )
        if mainPath.exists() and mainPath.is_dir():
            Myconsole.ok(
                msg="The main folder exist",
                show_console=show_console,
            )
        else:
            Myconsole.ko(
                msg="The main folder shall exist and be a directory",
                show_console=show_console,
            )
            return False

        # check the folder structure
        Myconsole.task(
            msg="Check Reqpy Folders Structure",
            show_console=show_console,
        )

        folders = FolderStructure(mainPath)

        if folders.all_foders_exist():
            Myconsole.ok(
                msg="All requested folders for reqpy exist ",
                show_console=show_console,
            )
        else:
            missingFolders = folders.get_missing_folders()

            missingFolders = [str(path.absolute()) for path in missingFolders]
            missingFolders = "\n".join(missingFolders)
            message = f"The following folders are missing :\n {missingFolders}"

            Myconsole.ko(
                msg=message,
                show_console=show_console,
            )
            return False
        return True
