""" Requirements class definition of reqpy and associated tools"""

# IMPORT SECTION
from __future__ import annotations
import yaml
from pathlib import Path
# from enum import auto, StrEnum
from datetime import datetime
from pydantic import BaseModel, Field, validator
from pydantic.json import pydantic_encoder
from .__settings import RequirementSettings, RequirementFileSettings
from .utils.validation import has_punctuation_or_accent


__all__ = [
    "Requirement",
    "ReqFile",
]

# ########################################################################## #
# ############################### UTILS CLASS ############################## #
# ########################################################################## #
# class ValidationStatus(StrEnum):
#     """
#     Enumeration representing the validation status of a requirement.

#     Attributes:
#         VALID: The requirement is valid.
#         UNVALID: The requirement is not yet validated.
#         INVALID: The requirement is invalid.

#     """
#     VALID = auto()
#     UNVALID = auto()
#     INVALID = auto()

# ########################################################################## #
# ############################ REQUIREMENT CLASS ########################### #
# ########################################################################## #


class Requirement(BaseModel):
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

    title: str = Field(
        min_length=RequirementSettings.min_title_length,
        max_length=RequirementSettings.max_title_length,
        default="Requirement Title"
    )
    detail: str = Field(
        max_length=RequirementSettings.max_detail_length,
        default="Description of the requirement as Markdown"
    )
    validation_status: str = "UNVALID"
    creation_date: datetime = datetime.now()

    @validator('validation_status')
    def status_is_conform(cls, value: str):
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
        if not title[0].isalpha():
            raise ValueError(
                'First character shall be an alphabet (a-z or A-Z).'
            )
        return title.capitalize()

    @validator("title")
    def title_must_contain_only_characters_or_figure(cls, title: str) -> str:
        if has_punctuation_or_accent(title):
            raise ValueError(
                f"Title property '{title}' shall be composed of numeric" +
                " and alpha characters, i.e. no punctuation or accent"
            )
        return title

    class Config:
        """Configuration class for the Requirement class.
        """
        allow_mutation = True  # allow mutation for the class Requirement
        validate_assignment = True  # activate the validation for assignement
        extra = 'forbid'  # unknow field is not permitted for the requirement


# ########################################################################## #
# ######################### REQUIREMENT FILE CLASS ######################### #
# ########################################################################## #


class ReqFile(BaseModel):
    """
    Represents a requirement file.

    Attributes:
        path (Path): Path of the requirements file. see pathlib.Path
    """

    path: Path  # path of the requirements files

    @validator("path")
    def validate_extension(cls, value):
        """
        Validates the extension of the file path.

        Args:
            value (str): The file path.

        Returns:
            str: The validated file path.

        Raises:
            ValueError: If the file path does not
             have an appropriate extension.
        """
        path = Path(value)
        file_extension = path.suffix.lower()
        if (file_extension != "" and
           file_extension in RequirementFileSettings.allowed_extensions):
            return path
        else:
            raise ValueError(
                f"The filepath {value} does not have an appropriate" +
                " extension, i.e " +
                f"[{RequirementFileSettings.allowed_extensions}]"
            )

    def exists(self) -> bool:
        """
        Checks if the requirement file exists.

        Returns:
            bool: True if the requirement file exists, False otherwise.
        """
        return self.path.exists()

    def read(self) -> Requirement:
        """
        Reads the requirement file and returns a Requirement object.

        Returns:
            Requirement: The Requirement object parsed from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if self.exists():
            with open(self.path, 'r') as file:
                datamap = yaml.safe_load(file)
            return Requirement(**datamap)
        raise FileNotFoundError(
            f"Impossible to read. The file {self.path} does not exist"
        )

    def write(self, requirement):
        """
        Writes a YAML file based on the Requirement object.

        Args:
            requirement (Requirement): The Requirement object to write.

        Returns:
            None

        Notes:
            - The writing of multiline string for YAML is updated.
            - This method uses pydantic_encoder to convert
              the Requirement object to JSON.
        """
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

        data_json = pydantic_encoder(requirement)

        with open(self.path, 'w+') as file:
            yaml.safe_dump(data_json, file)

    def get_valid_fileName(self):
        """
        Get the valid file name for the requirement file.

        Returns:
            str: The valid file name based on the requirement title.
        """
        requirement_title = self.read().title

        # Replace white space with _
        return requirement_title.replace(" ", "_")

    def is_valid_fileName(self):
        """
        Check if the file name is valid.

        Returns:
            bool: True if the file name is valid, False otherwise.
        """
        valid_name = self.get_valid_fileName()
        return self.path.stem == valid_name

    def rename_file(self) -> Path:
        """
        Rename the requirement file to a valid file name.

        Returns:
            (Path) new file
        """
        # Specify the folder path and the file name
        folder_path = self.path.parent
        new_file_name = (self.get_valid_fileName() + RequirementFileSettings.default_extension)

        # Create the Path objects for the new file
        new_file_path = folder_path / new_file_name

        # rename file
        self.path = self.path.rename(new_file_path)

        return new_file_path

    class Config:
        """Configuration class for the ReqFile class.
        """
        allow_mutation = True  # allow mutation for the class Requirement
        validate_assignment = True  # activate the validation for assignement
        extra = 'forbid'  # unknow field is not permitted for the reqfile
