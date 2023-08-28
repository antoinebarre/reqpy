"""All external API of Reqpy"""

from pathlib import Path

from .constants import DEFAULT_REQ_NAME, DEFAULT_REQPY_FILE_EXTENSION
from .requirement import Requirement, RequirementsSet

from .dirSkeleton import FolderStructure
from .__logging import Myconsole


class Apps():
    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(
            self,
            rootDir: Path) -> None:

        self.folderStructure = FolderStructure(rootDir)

    # ------------------------ INITIATE DATABASE ----------------------- #

    def initiate_database(
            self,
            show_console: bool = False
                      ) -> None:
        Myconsole.apps(
                msg="Initiate reqpy database",
                show_console=show_console,
            )
        try:
            if self.folderStructure.all_folders_exist():
                Myconsole.warning(
                    msg="All reqpy folders already exists",
                    show_console=show_console)
            else:
                self.folderStructure.create_folders()
                Myconsole.info(
                    msg="All reqpy folders are created",
                    show_console=show_console)
        except Exception as e:
            Myconsole.error(
                msg=(
                 f"Impossible to create reqpy folder due to :\n{str(e)}"
                )
            )
            raise e
    # ------------------------- RESET DATABASE ------------------------- #

    def reset_database(
            self,
            forced: bool = False,
            show_console: bool = False) -> bool:

        Myconsole.apps(
                msg="Reset reqpy database",
                show_console=show_console,
            )
        try:
            # Ask for user confirmation if it is not forced
            if forced is False:
                user_input = input(
                    "Are you sure you want to reset the existing file? (yes/no): "
                    ).lower()
            else:
                user_input = "yes"

            # Reset Database depending of the answer
            if user_input == 'yes' or user_input == 'y':
                # Reset the file
                self.folderStructure.reset_folders()

                Myconsole.info(
                    msg="All reqpy folders are reseted",
                    show_console=show_console)

                return False
            else:
                Myconsole.info(
                    msg="Reset is cancelled",
                    show_console=show_console)
                return True

        except Exception as e:
            Myconsole.error(
                msg=(
                 f"Impossible to reset reqpy folder due to :\n{str(e)}"
                )
            )
            raise e

    # -------------------------- FAKE DATABASE ------------------------- #

    def create_fake_database(
            self,
            show_console: bool = False,
            forced: bool = False
            ) -> bool:

        # reset existing database:
        if (self.reset_database(
             forced=forced,
             show_console=show_console)):

            Myconsole.info(
                msg="Creation of fake database cancelled by user"
            )
            return True

        Myconsole.apps(
                msg="Create Fake Database",
                show_console=show_console,
            )
        # create fake requirement
        Myconsole.task(
            msg="Create Fake Requirements",
            show_console=show_console)

        RequirementsSet(
            RequirementPath=self.folderStructure.requirements_folder
            ).createFakeRequirementsSet()

        return False

    # -------------------------- REQUIREMENTS -------------------------- #

    def create_new_requirement(
            self,
            show_console: bool = False):
        dir_path = self.folderStructure.requirements_folder

        Myconsole.apps(
                msg="Reset reqpy database",
                show_console=show_console,
            )
        try:
            reqf = Requirement.create_new_requirement(
                filePath=(
                 dir_path /
                 (DEFAULT_REQ_NAME + DEFAULT_REQPY_FILE_EXTENSION)
                )
            )
            Myconsole.info(
                msg=f"New requirement file created : { reqf.absolute()}",
                show_console=show_console,
            )
        except Exception as e:
            Myconsole.error(
                msg=(
                 f"Impossible to create a new requirement due to :\n{str(e)}"
                )
            )
            raise e
