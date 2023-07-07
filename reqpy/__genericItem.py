import logging
from pathlib import Path
from typing import Dict
import yaml
from .__settings import DEFAULT_EXTENSION


# import all option
__all__ = []

# logging
logger = logging.getLogger(__name__)


class ItemFileError(Exception):
    """Manage Requirement file exception."""
    pass


class ItemFolderError(Exception):
    """Manage Requirement folder exception."""
    pass


class GenericItem():

    # ------------------------------- CONSTRUCTOR -------------------------- #

    def _defaultExtension(self) -> str:
        return DEFAULT_EXTENSION

# ---------------------------------- TOOLS --------------------------------- #
    def _toStr(
            self,
            ObjectName: str = "Object",
              ) -> str:

        list_attributeName = self.__dict__.keys()  # list(vars(self).keys())

        attribute_Value = [
            (
             f"- {attributeName} : " +
             str(getattr(self, attributeName))
            ) for attributeName in list_attributeName]
        msg = (
            f">>> {ObjectName} Contents\n" +
            "\n".join(attribute_Value)
             )
        return msg

    def __toStrdict(self) -> Dict[str, str]:
        list_attributeName = list(vars(self).keys())

        return {
            attributeName: str(getattr(self, attributeName))
            for attributeName in list_attributeName
        }

    @staticmethod
    def is_valid_file_extension(
            filePath: Path,
            allowedExtension: str = DEFAULT_EXTENSION,
            ) -> bool:
        """
        Check if the file extension of a Path is valid to write a requirement.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            bool: True if the file extension is valid, False otherwise.

        """
        filePath = GenericItem.validatePath(filePath)

        # get file extension
        file_extension = filePath.suffix

        return (file_extension == allowedExtension)

# ---------------------------- VALIDATION TOOLS ---------------------------- #

    @staticmethod
    def validatePath(
            filePath: Path
            ) -> Path:
        """
        Validate if the input is a mutable file path.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            Path: The validated file path.

        Raises:
            TypeError: If the provided file path information is not mutable.

        """
        try:
            filePath = Path(filePath)
        except Exception as e:
            raise TypeError(
                "The provided file path information shall be mutable " +
                "to a pathlib.Path object. " +
                f"Following exception is raised:\n{str(e)}")
        return filePath

    @staticmethod
    def validateExistingFolder(
            folderPath: Path,
            ) -> Path:

        # create the Path to the file to write
        folderPath = GenericItem.validatePath(folderPath)

        if not folderPath.is_dir():
            # raise an error if the path is not an existing folder path
            msg = (
                f"The path {str(folderPath.absolute())}"
                " is not an existing folder path"
            )
            logger.error(msg)
            raise ItemFolderError(msg)
        return folderPath

    @staticmethod
    def validateCorrectFileExtension(
            filePath: Path,
            ) -> Path:

        if GenericItem.is_valid_file_extension(filePath):
            return filePath
        else:
            msg = (
                    f"The file [{str(filePath.absolute())}] does not have  "
                    "an allowed extension"
                    f"  (i.e. {DEFAULT_EXTENSION} )"
            )
            logger.error(msg)
            raise ItemFileError(msg)

    @staticmethod
    def validateExistingFile(
            filePath: Path
            ) -> Path:

        # check the extension
        filePath = GenericItem.validateCorrectFileExtension(filePath)

        if filePath.is_file():
            return filePath
        else:
            msg = f"The file {filePath.absolute()} does not exist"
            logger.error(msg)
            raise ItemFileError(msg)

# -------------------------------- I/O FILES ------------------------------- #
    def _generic_write(
            self,
            filePath: Path = Path(),
            ) -> Path:

        # validate filePath extension
        filePath = self.validateCorrectFileExtension(filePath)

        # create a presenter for multiline
        def str_presenter(dumper, data):
            """Configures YAML for dumping multiline strings."""
            if data.count('\n') > 0:  # check for multiline string
                return dumper.represent_scalar(
                    'tag:yaml.org,2002:str',
                    data,
                    style='|'
                    )
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        yaml.add_representer(str, str_presenter)
        yaml.representer.SafeRepresenter.add_representer(
            str, str_presenter)  # to use with safe_dump

        data = self.__toStrdict()

        with open(filePath, 'w+') as file:
            yaml.safe_dump(data, file)

        logger.debug(
            f"The file {filePath} is created"
        )
        return filePath

    @staticmethod
    def read2dict(filePath: Path) -> Dict:
        """
        Read a file to extract the requirement object.

        Args:
            filePath (Path): The file path to read.

        Returns:
            Requirement: The extracted requirement object.

        Raises:
            RequirementFileError: If the file does not exist
              or has an invalid extension.

        """

        # validate filePath
        filePath = GenericItem.validateExistingFile(filePath)

        try:
            with open(filePath, 'r') as file:
                datamap = yaml.safe_load(file)
            return datamap
        except Exception as e:
            raise ItemFileError(
                f"Impossible to parse the YAML file {filePath.absolute()}" +
                f"due to : {str(e)}"
                )
