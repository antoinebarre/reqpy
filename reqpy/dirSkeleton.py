

from pathlib import Path
import shutil
from pydantic import BaseModel, ConfigDict
from .settings import FoldersSettings
from loguru import logger as log


class FolderStructure(BaseModel):
    # ------------------------------ MODEL ----------------------------- #
    main_folder: Path
    requirements_folder: Path
    definition_folder: Path
    references_folder: Path

    # ----------------------------- CONFIG ----------------------------- #

    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(self, currentFolderPath: Path = Path()):
        """Constructor for the FolderStructure class.

        Args:
            currentFolderPath (Path): The current folder path. Defaults to
              an empty Path object.

        """

        # the main folder shall exist
        if not currentFolderPath.exists():
            raise FileExistsError(
                f"The folder {currentFolderPath} doesnt exist"
            )

        main_folder = currentFolderPath / FoldersSettings.main_folder_name

        super().__init__(
            main_folder=main_folder,
            requirements_folder=(main_folder /
                                 FoldersSettings.requirements_folder_name),
            definition_folder=(main_folder /
                               FoldersSettings.definitions_folder_name),
            references_folder=(main_folder /
                               FoldersSettings.references_folder_name),
        )

    # --------------------------- PROPERTIES --------------------------- #
    @property
    def foldersList(self) -> list[Path]:
        """Get the list of folders.

        Returns:
            List[Path]: The list of folders.

        """
        return [info[1] for info in list(self)]

    def get_missing_folders(self) -> list[Path]:
        """Get the list of missing folders.

        Returns:
            List[Path]: The list of missing folders.

        """
        return [folder for folder in self.foldersList if not folder.exists()]

    def all_folders_exist(self) -> bool:
        """Check if all folders exist.

        Returns:
            bool: True if all folders exist, False otherwise.

        """
        if bool(self.get_missing_folders()):
            return False
        else:
            return True

    # -------------------------- CREATE/REMOVE ------------------------- #
    @log.catch
    @staticmethod
    def create_gitignore_file(directory: Path) -> Path:
        gitignore_path = Path(directory) / ".gitignore"
        gitignore_content = "# Add your gitignore rules here"

        # Create the .gitignore file
        gitignore_path.write_text(gitignore_content)

        # logging
        msg = (
            f"Created .gitignore file at: {gitignore_path.absolute()}")
        log.debug(msg)

        return gitignore_path

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
