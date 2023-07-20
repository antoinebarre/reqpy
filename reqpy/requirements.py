""" Requirements class definition of reqpy and associated tools"""

# IMPORT SECTION
from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field, validator
from .__settings import RequirementSettings, DEFAULT_EXTENSION_REPORT
from .tools.__string import has_punctuation_or_accent
from .__genericItem import GenericItem
from .__DB import GenericSubDB, FileError
from .folders import FolderStructure
from loguru import logger as log
from .__logging import Myconsole
from .markdown import MDText


__all__ = [
    "Requirement",
    "RequirementFolder",
]

# TODO : add DEFAULT_DESCRIPTION


class RequirementError(Exception):
    pass


class Requirement(BaseModel, GenericItem):
    """
    Represents a requirement with title, content, validation status,
    and creation date.

    Attributes:
        title (str): The title of the requirement.
        description (str): The content of the requirement.
        validation_status (ValidationStatus): The validation status of
         the requirement.
        creation_date (datetime): The creation date of the requirement.

    """

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
            description: str = "Description of the requirement as Markdown",
            rationale: str = "Rationale of the requirement",
            validation_status: str = "UNVALID",
            **kwargs
            ):

        super().__init__(
            title=title,
            description=description,
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
            raise RequirementError(
                f"Impossible to parse the YAML file {filePath}" +
                f" due to this error: \n{str(e)}"
            )
        return new_req

    @log.catch(reraise=True)
    def write(
            self,
            folderPath: Path = Path(),
            ) -> Path:

        # validate folderPath
        folderPath = Requirement.validateExistingFolder(folderPath)

        # build the filename
        fileName = (self.get_valid_fileName() +
                    self._defaultExtension)

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

# -------------------------- EXPORT TOOLS -------------------------- #
    def toMD(self) -> str:

        listOfAttributes = self.listAttributes()

        # initiate MK object
        mk = MDText()

        # create title
        mk.add_title(self.title)

        # create paragraphs
        for attribute in listOfAttributes:
            if attribute != "title":
                mk.add_header(level=2,title=attribute.upper())
                mk.add_paragraph(text=getattr(self, attribute))
        return str(mk)

    def toMDFile(
            self,
            directoryPath: Path
            ) -> Path:

        newMDFile = directoryPath / (
            self.get_valid_fileName() +
            DEFAULT_EXTENSION_REPORT
            )
        # create directory if necessary
        directoryPath.mkdir(parents=True, exist_ok=True)

        # write file
        with newMDFile.open("w+", encoding="utf-8") as f:
            f.write(self.toMD())

        return newMDFile


class RequirementFolder(GenericSubDB):
    def __init__(self, mainFolder: Path = Path()):

        # get the Reqpy folders structure
        foldersStructure = FolderStructure(mainFolder)

        super().__init__(
            folderPath=mainFolder / foldersStructure.requirements_folder,
            allowedExtensions=[Requirement._defaultExtension],
            allowSubfolders=True,
            allowAdditionalFiles=True)

# -------------------------- EXPORT TOOLS -------------------------- #

    @log.catch(reraise=True)
    def generate_MD(
            self,
            MDPath: Path,
            show_console: bool = False
            ):
        # console
        Myconsole.apps(
            msg="Generate Markdow Files :",
            show_console=show_console,
        )

        # target info :
        msg = f"Targeted Folder:{str(MDPath.absolute())}"
        Myconsole.info(
            msg=msg,
            show_console=show_console,
        )
        log.trace(msg)

        # list files
        list_files = self.list_valid_files()

        # logging
        infoList = [str(fileName.absolute()) for fileName in list_files]
        log.trace(
            f"List of Yaml Files :\n {infoList}")
        Myconsole.info(
            msg=f"Number of files to generate: {len(list_files)}",
            show_console=show_console
        )

        # create the progress bar
        sequence = Myconsole.progressBar(
            sequence=list_files,
            description="Generate Markdown files...",
            show_console=show_console
        )

        for filePath in sequence:

            req = Requirement.read(
                filePath=filePath)

            newMDFolder = MDPath / filePath.relative_to(self.folderPath).parent

            newFile = req.toMDFile(
                directoryPath=newMDFolder,
            )
            # Logging
            log.trace(f"Created Markdown file: {newFile}")

        # copy additional files
        self.copy_additional_files(
            destinationDir=MDPath,
            show_console=show_console)

    # ========================== VALIDATIONS STATUS ========================= #

    @log.catch(reraise=True)
    def generate_status(
            self,
            show_console: bool = True,
            ) -> list[FileError]:

        Myconsole.apps(
            msg="Generate Requirement Files status :",
            show_console=show_console,
        )

        # list files
        list_files = self.list_valid_files()

        # logging
        infoList = [str(fileName.absolute()) for fileName in list_files]
        log.trace(
            f"List of Yaml Files to inspect :\n {infoList}")
        Myconsole.info(
            msg=f"Number of files to inspect: {len(list_files)}",
            show_console=show_console
        )

        # create the progress bar
        sequence = Myconsole.progressBar(
            sequence=list_files,
            description="Inspect Requirement files...",
            show_console=show_console
        )

        # Initiate the outputs
        errorStatus = []

        for file in sequence:
            try:
                Requirement.read(filePath=file)
                log.trace(
                    f"OK for {file}"
                )
            except Exception as e:

                msg = f"KO for {file} due to :\n{str(e)}"

                log.trace(msg)
                Myconsole.ko(
                    msg=msg,
                    show_console=show_console,
                )

                errorStatus.append(
                    FileError(
                        filePath=file,
                        errorMsg=str(e)
                    )
                )
        return errorStatus
