"""Definition of Requirement Class"""

# IMPORT SECTION
from __future__ import annotations
from loguru import logger as log
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .__genericItem import GenericItem
from .settings import RequirementSettings
from .exception import ReqpyIOException
from .tools.strings import has_punctuation_or_accent

from .requirementItems import ValidationStatus

__all__ = [
    "Requirement",
]


class Requirement(BaseModel, GenericItem):

    # ------------------------------- ATTRIBUTES ------------------------- #
    title: str = Field(
        min_length=RequirementSettings.min_title_length,
        max_length=RequirementSettings.max_title_length
    )
    description: str = Field(
        max_length=RequirementSettings.max_description_length,
        default="Description of the requirement as Markdown"
    )
    rationale: str = Field(
        default=(
            "Rationale of the requirement"
            )
    )

    validation_status: ValidationStatus = ValidationStatus.UNVALID

    # -------------------------- CONFIGURATION ------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=False,
        )
    # --------------------------- CONSTRUCTOR -------------------------- #

    def __init__(
            self,
            title: str,
            description: str = "Description of the requirement as Markdown",
            rationale: str = "Rationale of the requirement",
            validation_status: ValidationStatus = ValidationStatus.UNVALID,
            **kwargs
            ):

        super().__init__(
            title=title,
            description=description,
            rationale=rationale,
            validation_status=validation_status,
            **kwargs
        )

    # ------------------------- DUNDER METHODS ------------------------- #
    def __str__(self):
        return GenericItem.__str__(self)

    # --------------------------- VALIDATION --------------------------- #

    @field_validator('title')
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

    @field_validator("title")
    def title_must_contain_only_characters_or_figures(cls, title: str) -> str:
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

# -------------------------- READ / WRITE TOOLS ------------------------- #

    @log.catch(reraise=True)
    @staticmethod
    def read(
            filePath: Path,
            ) -> Requirement:

        data = Requirement.read2dict(
            filePath=filePath)
        try:
            new_req = Requirement(**data)
        except Exception as e:
            raise ReqpyIOException(
                f"Impossible to parse the YAML file {filePath}" +
                f" due to this error: \n{str(e)}"
            )
        return new_req

# ---------------------- FILE VALIDATION TOOLS --------------------- #

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

# # -------------------------- EXPORT TOOLS -------------------------- #
#     def toMD(self) -> str:

#         listOfAttributes = self.listAttributes()

#         # initiate MK object
#         mk = MDText()

#         # create title
#         mk.add_title(self.title)

#         # create paragraphs
#         for attribute in listOfAttributes:
#             if attribute != "title":
#                 mk.add_header(level=2,title=attribute.upper())
#                 mk.add_paragraph(text=getattr(self, attribute))
#         return str(mk)

#     def toMDFile(
#             self,
#             directoryPath: Path
#             ) -> Path:

#         newMDFile = directoryPath / (
#             self.get_valid_fileName() +
#             DEFAULT_EXTENSION_REPORT
#             )
#         # create directory if necessary
#         directoryPath.mkdir(parents=True, exist_ok=True)

#         # write file
#         with newMDFile.open("w+", encoding="utf-8") as f:
#             f.write(self.toMD())

#         return newMDFile
