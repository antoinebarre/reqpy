""" Requirements class definition of reqpy and associated tools"""

# IMPORT SECTION
from __future__ import annotations
import logging
from pathlib import Path
from pydantic import BaseModel, Field, validator
from .__settings import RequirementSettings
from .utils.validation import has_punctuation_or_accent
from .__genericItem import GenericItem


__all__ = [
    "Requirement",
]

# TODO : add DEFAULT_DESCRIPTION


# logger for logging
logger = logging.getLogger(__name__)


class RequirementError(Exception):
    pass


class Requirement(BaseModel, GenericItem):
    """
    Represents a requirement with title, content, validation status,
    and creation date.

    Attributes:
        title (str): The title of the requirement.
        detail (str): The content of the requirement.
        validation_status (ValidationStatus): The validation status of
         the requirement.
        creation_date (datetime): The creation date of the requirement.

    """

    # ------------------------------- ATTRIBUTES ------------------------- #
    title: str = Field(
        min_length=RequirementSettings.min_title_length,
        max_length=RequirementSettings.max_title_length
    )
    detail: str = Field(
        max_length=RequirementSettings.max_detail_length,
        default="Description of the requirement as Markdown"
    )
    rationale: str = Field(
        default=(
            "Rationale of the requirement"
            )
    )

    validation_status: str = "UNVALID"

    class Config:
        """Configuration class for the Requirement class.
        """
        allow_mutation = True  # allow mutation for the class Requirement
        validate_assignment = True  # activate the validation for assignement
        extra = 'forbid'  # unknow field is not permitted for the requirement

    # ------------------------------- CONSTRUCTOR ------------------------#

    def __init__(
            self,
            title: str,
            detail: str = "Description of the requirement as Markdown",
            rationale: str = "Rationale of the requirement",
            validation_status: str = "UNVALID",
            **kwargs
            ):

        super().__init__(
            title=title,
            detail=detail,
            rationale=rationale,
            validation_status=validation_status,
            **kwargs
        )

    def __str__(self):
        return self._toStr(
            ObjectName="Requirement",
        )

    # ----------------------------- VALIDATORS ----------------------------- #

    @validator('validation_status')
    def status_is_conform(cls, value: str):
        """
        Validate if the validation status is conform.

        Args:
            cls: The class object.
            value (str): The validation status value.

        Returns:
            str: The validated validation status.

        Raises:
            ValueError: If the validation status is not in the permitted list.

        """

        if value.upper() in RequirementSettings.validation_status:
            return value.upper()
        else:
            raise ValueError(
                f"Validation status [{value}] is not in" +
                f" the permitted list {RequirementSettings.validation_status}"
                             )

    @validator('title')
    def title_must_start_with_alpha(cls, title: str) -> str:
        """
        Validates that the title starts with an alphabet character.

        Args:
            cls: The class object.
            title (str): The title to validate.

        Returns:
            str: The capitalized title.

        Raises:
            ValueError: If the first character of the title is not an alphabet.

        """
        if not title[0].isalpha() or not title[0].isupper():
            raise ValueError(
                (
                 'First character shall be an upper case letters (A-Z). '
                 f'Current: {title}'
                 )
            )
        return title

    @validator("title")
    def title_must_contain_only_characters_or_figure(cls, title: str) -> str:
        """
        Validate if the title contains only alphanumeric characters.

        Args:
            cls: The class object.
            title (str): The title to validate.

        Returns:
            str: The validated title.

        Raises:
            ValueError: If the title contains punctuation or accent characters.

        """
        if has_punctuation_or_accent(title):
            raise ValueError(
                f"Title property '{title}' shall be composed of numeric" +
                " and alpha characters, i.e. no punctuation or accent"
            )
        return title

# ------------------------------ FILE NAME ------------------------------ #

    def get_valid_fileName(self) -> str:
        """
        Provide the appropriate file name according to the requirement title.

        Returns:
            str: The valid file name.

        """
        return self.title.replace(" ", "_")

    def is_valid_fileName(
            self,
            filePath: Path
            ) -> bool:
        """
        Check if the file name is valid.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            bool: True if the file name is valid, False otherwise.

        """
        filePath = self.validateCorrectFileExtension(filePath)

        valid_name = self.get_valid_fileName()
        return filePath.stem == valid_name

# -------------------------- READ / WRITE TOOLS ------------------------- #

    @staticmethod
    def read(
            filePath: Path,
            ) -> Requirement:

        data = Requirement.read2dict(
            filePath=filePath)
        try:
            new_req = Requirement(**data)
        except Exception as e:
            raise RequirementError(
                f"Impossible to parse the YAML file {filePath}" +
                f" due to this error: \n{str(e)}"
            )
        return new_req

    def write(
            self,
            folderPath: Path = Path(),
            ) -> Path:

        # validate folderPath
        folderPath = self.validateExistingFolder(folderPath)

        # build the filename
        fileName = (self.get_valid_fileName() +
                    self._defaultExtension())

        # build the file path
        filePath = folderPath / fileName

        self._generic_write(
            filePath=filePath,
            )
        return filePath

# ------------------------ FILE VALIDATION TOOLS ------------------------ #
    @staticmethod
    def get_file_Errors(
         filePath: Path
         ) -> str:
        """
        Get a list of errors found in the requirement file.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            List[str]: The list of errors found in the file.

        """
        try:
            Requirement.read(
                filePath=filePath
            )
            return ''
        except Exception as e:
            errorMsg = str(e)
            return errorMsg

    @staticmethod
    def is_ValidRequirementFile(
         filePath: Path
         ) -> bool:
        if Requirement.get_file_Errors(filePath) == "":
            return True  # List is not empty
        else:
            return False

    @staticmethod
    def is_valid_RequirementFile_Name(
        filePath: Path
    ) -> bool:
        """
        Check if the file has a valid requirement file name.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            bool: True if the file name is valid, False otherwise.

        """
        return Requirement.read(filePath).is_valid_fileName(filePath)

    @staticmethod
    def get_fileName_error(
                filePath: Path,
                ) -> str:
        if Requirement.read(filePath).is_valid_fileName(filePath):
            return ""
        else:
            validName = Requirement.read(filePath).get_valid_fileName()
            msg = (
                "The file has an invalid file name\n"
                f"Current Name : {filePath.stem}\n"
                f"Valid Name: {validName}"
                )
            return msg
