""" Package with Hig level function of the reqpy package """

from pathlib import Path
import reqpy
from reqpy.database import ReqFolder
import logging
import reqpy.folders
from reqpy.utils import generate_random_string, randomText
from reqpy.requirements import Requirement
from faker import Faker
from reqpy.__logging import with_logging, printConsole


__all__ = [
    "init_reqpy",
    "reset_reqpy",
    "generate_fakeDB",
    "validate_reqpy_database",
]

# logger and console for logging
logger = logging.getLogger(__name__)


def validate_reqpy_database(
        mainPath: Path = Path(),
        show_console: bool = True,
        ) -> bool:

    printConsole(
        message='Validate REQPY database',
        show_console=show_console,
        type="TITLE"
    )

    res = []

    res_temp = reqpy.folders.FolderStructure.validate_folders_structure(
            mainPath=mainPath,
            show_console=show_console)

    res.append(res_temp)

    res_temp = reqpy.folders.RequirementFolder().validateFolder(
        mainPath=mainPath,
        show_console=show_console)
    res.append(res_temp)

    return all(res)


@with_logging
def reset_reqpy(
 folder: Path = Path(),
 show_console: bool = True
 ) -> None:
    printConsole(
        message="Reset reqpy database",
        show_console=show_console,
        type="APPS"
    )

    try:
        printConsole(
            message=(
                f"The path provided is {folder.absolute()}"
                f" [type: {type(folder)}]"
            ),
            type="INFO",
            show_console=show_console
            )

        t = reqpy.folders.FolderStructure(currentFolderPath=folder)

        # create the folder:
        t.reset_folders()

        printConsole(
            message="Requirement database is reseted successfuly !",
            type="OK",
            show_console=show_console
        )

    except Exception as E:
        printConsole(
            message="Requirement database is not reseted",
            type="KO",
            show_console=show_console
        )
        logging.exception(
            "Exception occurred during the requirement"
            " project initialization :\n",
            str(E)
            )


@with_logging
def init_reqpy(folder: Path = Path()) -> None:
    """
    Initialize the reqpy requirement project.

    Args:
        folder (Path, optional): The root folder path. Defaults to Path().

    Returns:
        None

    Raises:
        Exception: If an exception occurs during the requirement
          project initialization.
    """
    try:
        logging.debug(
            f"The path provided is {str(folder)} [type: {type(folder)}]"
            )
        t = ReqFolder(rootdir=folder)

        # create the folder:
        t.create_dirs()

    except Exception:
        logging.exception(
            "Exception occurred during the requirement project initialization"
            )


@with_logging
def generate_fakeDB(
        nbFilesPerFolder: int = 10,  # number of files per folder
        nbFolder: int = 5,  # number of additional folder in requirement
        path: Path = Path()  # path where the DB is created
 ) -> None:

    # Get the Database folder structure
    Folders = reqpy.folders.FolderStructure(currentFolderPath=path)

    # create folders
    Folders.delete_folders()
    Folders.create_folders()

    # create a fake instance
    fake = Faker()

    # create a list of requirement folders
    list_folders = [
         Folders.requirements_folder / generate_random_string(30)
         for _ in range(nbFolder)
        ]
    list_folders.append(Folders.requirements_folder)

    for folder in list_folders:
        # create folder
        folder.mkdir(exist_ok=True)

        for _ in range(nbFilesPerFolder):
            req = Requirement(
                title=generate_random_string(40).capitalize(),
                detail=fake.text(max_nb_chars=2000),
                rationale=randomText(),
                )
            req.write(
                folderPath=folder
            )
