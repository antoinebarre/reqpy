from loguru import logger as log
from pathlib import Path
from typing import Dict
from pydantic import BaseModel
import yaml
from .__settings import DEFAULT_EXTENSION


# import all option
__all__ = []


class ItemFileError(Exception):
    """Manage Requirement file exception."""
    pass


class ItemFolderError(Exception):
    """Manage Requirement folder exception."""
    pass


class GenericItem():
    _defaultExtension = DEFAULT_EXTENSION
    # ------------------------------- CONSTRUCTOR -------------------------- #

    def listAttributes(self) -> list[str]:
        return list(vars(self).keys())

# ---------------------------------- TOOLS --------------------------------- #
    def _toStr(
            self,
            ObjectName: str = "Object",
              ) -> str:

        list_attributeName = self.listAttributes()

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
        list_attributeName = self.listAttributes()

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
    @log.catch(reraise=True)
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

    @log.catch(reraise=True)
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
            raise ItemFolderError(msg)
        return folderPath

    @log.catch(reraise=True)
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
            raise ItemFileError(msg)

    @log.catch(reraise=True)
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
            raise ItemFileError(msg)

# -------------------------------- I/O FILES ------------------------------- #
    @log.catch(reraise=True)
    def _generic_write(
            self,
            filePath: Path = Path(),
            ) -> Path:

        # validate filePath extension
        filePath = GenericItem.validateCorrectFileExtension(filePath)

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
            yaml.safe_dump(data, file,
                           sort_keys=False)

        log.trace(
            f"The file {filePath} is created"
        )
        return filePath

    @log.catch(reraise=True)
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


class MarkdownContents(BaseModel):
    content: str

    class Config:
        """Configuration class for the Requirement class.
        """
        allow_mutation = True  # allow mutation for the class Requirement
        validate_assignment = True  # activate the validation for assignement
        extra = 'forbid'  # unknow field is not permitted for the requirement
