""" Requirements class definition of reqpy and associated tools"""

# IMPORT SECTION
from __future__ import annotations
import yaml
import logging
from pathlib import Path
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from pydantic.json import pydantic_encoder
from .__settings import RequirementSettings, RequirementFileSettings
from .utils.validation import has_punctuation_or_accent


__all__ = [
    "Requirement",
]

# ############################ CUSTOM EXCEPTIONS ########################### #


class RequirementFileError(Exception):
    """Manage Requirement file exception."""
    pass


class RequiqrementFolderError(Exception):
    """Manage Requirement folder exception."""
    pass

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
    rationale: str = Field(
        default="Rationale of the requirement"
    )

    validation_status: str = "UNVALID"
    creation_date: datetime = datetime.now()

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
                'First character shall be an upper case letters (A-Z).'
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

    class Config:
        """Configuration class for the Requirement class.
        """
        allow_mutation = True  # allow mutation for the class Requirement
        validate_assignment = True  # activate the validation for assignement
        extra = 'forbid'  # unknow field is not permitted for the requirement

# ############################## FILE HANDLING ############################# #

    def get_valid_fileName(self) -> str:
        """
        Provide the appropriate file name according to the requirement title.

        Returns:
            str: The valid file name.

        """

        return (self.title.replace(" ", "_") +
                RequirementFileSettings.default_extension)

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
        filePath = self.validatePath(filePath)

        valid_name = self.get_valid_fileName()
        return filePath.name == valid_name

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
    def is_valid_file_extension(
            filePath: Path
            ) -> bool:
        """
        Check if the file extension of a Path is valid to write a requirement.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            bool: True if the file extension is valid, False otherwise.

        """
        filePath = Requirement.validatePath(filePath)
        # get file extension
        file_extension = filePath.suffix

        return (
            file_extension != "" and
            file_extension in RequirementFileSettings.allowed_extensions)

# ########################### READ / WRITE TOOLS ########################### #

    @staticmethod
    def read(filePath: Path) -> Requirement:
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
        if (
            Requirement.is_valid_file_extension(filePath=filePath) and
            filePath.is_file()
        ):
            with open(filePath, 'r') as file:
                datamap = yaml.safe_load(file)
            return Requirement(**datamap)
        else:
            msg = (
                f"The file [{str(filePath.absolute())}] does not exist "
                "or the file extension is not an allowed extension"
                f"  (i.e. {RequirementFileSettings.allowed_extensions} )"
            )
            raise RequirementFileError(msg)

    def write(
            self,
            folderPath: Path = Path(),
            ) -> Path:
        """
        Write the requirement in a YAML file with the appropriate name.

        Args:
            folderPath (Path, optional): The folder path to write the file.
                Defaults to Path().

        Returns:
            Path : path of the created file

        Raises:
            RequiqrementFolderError: If the path is not
            an existing folder path.

        """

        # create the Path to the file to write
        folderPath = self.validatePath(folderPath)

        if not folderPath.is_dir():
            # raise an error if the path is not an existing folder path
            msg = (
                f"The path {str(folderPath.absolute())}"
                " is not an existing folder path"
            )
            logging.error(msg)
            raise RequiqrementFolderError(msg)

        fileName = self.get_valid_fileName()
        filePath = folderPath / fileName

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

        data_json = pydantic_encoder(self)

        with open(filePath, 'w+') as file:
            yaml.safe_dump(data_json, file)

        logging.info(
            f"The requirement file {filePath} is created"
        )
        return filePath

    @staticmethod
    def rename(
         filePath: Path
         ) -> Path:
        """
        Rename the requirement file if necessary.

        Args:
            filePath (Path): The file path to rename.

        Returns:
            Path: The new file path after renaming.

        Raises:
            RequirementFileError: If the file is not a requirement file.

        """

        if not Requirement.is_RequirementFile(filePath):
            msg = (
                f"The file {str(filePath.absolute())} is "
                "not a requirement file"
            )
            logging.error(msg)
            raise RequirementFileError(msg)

        if not Requirement.is_valid_RequirementFile_Name(filePath):
            # Specify the folder path and the new file name
            folder_path = filePath.parent
            new_file_name = Requirement.read(filePath).get_valid_fileName()

            # Create the Path objects for the new file
            new_file_path = folder_path / new_file_name

            # rename file
            new_file_path = filePath.rename(new_file_path)
            logging.info(
                (
                 f"Rename of the file {filePath} to {new_file_path}"
                )
            )
            return new_file_path
        else:
            logging.warning(
                (f"The file {filePath} has the already "
                 "the right name - no action ")
                 )
            return filePath

# ########################## FILE VALIDATION TOOLS ######################### #

    @staticmethod
    def get_file_Errors(
         filePath: Path
         ) -> List[str]:
        """
        Get a list of errors found in the requirement file.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            List[str]: The list of errors found in the file.

        """

        # Initiate errors list
        errors: List[str] = []

        # check if the file exist
        if not filePath.is_file():
            msg: str = (
                f"The path {str(filePath)} is not an existing file"
            )
            errors.append(msg)
            return errors

        # check if an appropriate extension
        if not Requirement.is_valid_file_extension(filePath):
            msg: str = (
                f"The extension {filePath.suffix} is not valid"
            )
            errors.append(msg)
            return errors

        # Impossible to map the yaml file
        try:
            Requirement.read(
                filePath=filePath,
                )
        except Exception as e:
            msg = (
                "The formating of the files is not "
                "correct with the following problems:\n"
                f"{str(e)}"
            )
            errors.append(msg)

        return errors

    @staticmethod
    def is_RequirementFile(
         filePath: Path
         ) -> bool:
        """
        Check if the file is a valid requirement file.

        Args:
            filePath (Path): The file path to validate.

        Returns:
            bool: True if the file is a requirement file, False otherwise.

        """
        if len(Requirement.get_file_Errors(filePath)):
            return False  # List is not empty
        else:
            return True

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
