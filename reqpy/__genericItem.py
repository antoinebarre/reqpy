import builtins
from loguru import logger as log
from pathlib import Path
from typing import Any, Dict
import yaml
from .constants import DEFAULT_REQPY_FILE_EXTENSION
from .tools.paths import (validateCorrectFileExtension,
                          validateFileExistence)
from .exception import ReqpyIOException


# import all option
__all__ = []


class GenericItem():
    """
    GenericItem class for basic functionality.

    Attributes:
        _defaultExtension (str): Default file extension.

    """
    _defaultExtension = DEFAULT_REQPY_FILE_EXTENSION

    # --------------------------- CONSTRUCTOR -------------------------- #

    # ------------------------- DUNDER METHODS ------------------------- #

    def __str__(self) -> str:
        """
        Generate a string representation of the object.

        Returns:
            str: String representation of the object.

        """
        list_attributeName = self.attributesList

        attribute_Value = [
            (
             f"- {attributeName} : " +
             str(getattr(self, attributeName))
            ) for attributeName in list_attributeName]
        msg = (
            f">>> {self.className} Contents\n" +
            "\n".join(attribute_Value)
             )
        return msg

    # --------------------------- PROPERTIES --------------------------- #
    @property
    def attributesList(self) -> list[str]:
        """
        Get a list of attributes of the object.

        Returns:
            list[str]: List of attribute names.

        """
        return list(vars(self).keys())

    @property
    def className(self) -> str:
        """
        Get the class name of the object.

        Returns:
            str: Class name of the object.

        """
        return self.__class__.__name__

# ---------------------------------- TOOLS --------------------------------- #

    def toDict(self) -> Dict[str, Any]:
        """
        Convert object attributes to a dictionary for YAML export.

        Returns:
            Dict[str, Any]: Dictionary containing attribute names and values.

        """
        list_attributeName = self.attributesList
        outDict = {}
        for attributeName in list_attributeName:
            attr_value = getattr(self, attributeName)

            if type(attr_value).__name__ in dir(builtins):
                outDict[attributeName] = attr_value
            else:
                outDict[attributeName] = str(attr_value)
        return outDict

# -------------------------------- I/O FILES ------------------------------- #

    @log.catch(reraise=True)
    def write(
            self,
            filePath: Path,
            ) -> Path:
        """
        Write object attributes to a YAML file.

        Args:
            filePath (Path): File path to write.

        Returns:
            Path: Path of the written file.

        """

        # validate filePath extension
        filePath = validateCorrectFileExtension(
            filePath,
            allowedExtension=DEFAULT_REQPY_FILE_EXTENSION)

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

        data = self.toDict()

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
        Read a file and extract the requirement object data.

        Args:
            filePath (Path): File path to read.

        Returns:
            Dict: Extracted data from the file.

        Raises:
            ReqpyIOException: If the file does not exist or has an invalid
            extension.

        """

        # validate filePath
        filePath = validateFileExistence(filePath)

        try:
            with open(filePath, 'r') as file:
                datamap = yaml.safe_load(file)
            return datamap
        except Exception as e:
            raise ReqpyIOException(
                f"Impossible to parse the YAML file {filePath.absolute()}" +
                f"due to : {str(e)}"
                )
