"""Definition of Requirement Class"""

# IMPORT SECTION
from __future__ import annotations
import os
import random
from loguru import logger as log
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .tools.paths import validateCorrectFileExtension, Directory

from .constants import DEFAULT_REQPY_FILE_EXTENSION, DEFAULT_REPORT_EXTENSION
from .tools.image import generate_random_image
from .tools.markdown import MDText
from .tools.status import (CheckStatus, CheckStatusList,
                           FileStatus, FileStatusList)
from .__logging import Myconsole

from .__genericItem import GenericItem
from .__DB import GenericDB
from .settings import RequirementSettings
from .exception import ReqpyDBException, ReqpyIOException
from .tools.strings import (
    generate_paragraph,
    has_punctuation_or_accent,
    random_Title,
    random_string)

from .requirementItems import ValidationStatus

__all__ = [
    "Requirement",
    "RequirementsSet"
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

    # ------------------------ FAKE REQUIREMENT ------------------------ #
    @staticmethod
    def createFakeRequirement() -> Requirement:
        return Requirement(
            title=random_Title(
                min_length=RequirementSettings.min_title_length,
                max_length=RequirementSettings.max_title_length
                ),
            description=generate_paragraph(
                max_characters=RequirementSettings.max_description_length
            ),
            rationale=generate_paragraph(
                max_characters=RequirementSettings.max_description_length
            )
        )

    @staticmethod
    def writeFakeRequirementFile_withPictures(
            filePath: Path,
            ) -> Path:

        # create fake Requirement
        req = Requirement.createFakeRequirement()

        # Create image path
        dirPath = filePath.parent
        fileName = filePath.stem
        imgPath1 = dirPath / (fileName + "_1.jpg")
        imgPath2 = dirPath / (fileName + "_2.jpg")

        # generate two images (200x200pixels)
        img1 = generate_random_image(200, 200)
        img1.save(imgPath1, "JPEG")
        img2 = generate_random_image(200, 200)
        img2.save(imgPath2, "JPEG")

        # modify requirement
        req.description += f"\n[IMG TEST 01]({imgPath1.name})\n"
        req.rationale += f"\n[IMG TEST 02]({imgPath2.name})\n"

        # write file
        filePath = req.write(
            filePath=filePath,
            )
        return filePath

    @staticmethod
    def writeFakeRequirementFile(
            filePath: Path,
            ) -> Path:

        # create fake Requirement
        req = Requirement.createFakeRequirement()

        # write file
        filePath = req.write(
            filePath=filePath,
            )
        return filePath
# ---------------------- FILE VALIDATION TOOLS --------------------- #

    @staticmethod
    def validateRequirementFile(
            filePath: Path
            ) -> CheckStatus:
        """
        Validates the given requirement file.

        This method reads the content of a requirement file and attempts to
        create a `Requirement` instance from it. If successful, it returns a
        `CheckStatus` object indicating that the file is valid. If the content
        cannot be parsed or if an exception occurs during the instantiation of
        the `Requirement` instance, the method returns a `CheckStatus` object
        indicating that the file is invalid and includes the error message.

        Args:
            filePath (Path): The path to the requirement file to be validated.

        Returns:
            CheckStatus: A `CheckStatus` object indicating whether the file is
                        valid and containing any error messages if applicable.
        """

        checkName = "Validates the requirement file"

        try:
            Requirement.read(
                filePath=filePath
            )
            return CheckStatus.createValid(checkName=checkName)

        except Exception as e:
            errorMsg = str(e)
            return CheckStatus(
                checkName=checkName,
                valid=False,
                message=errorMsg
            )

    # @staticmethod
    # def get_file_Errors(
    #      filePath: Path
    #      ) -> str:
    #     """
    #     Get a list of errors found in the requirement file.

    #     Args:
    #         filePath (Path): The file path to validate.

    #     Returns:
    #         List[str]: The list of errors found in the file.

    #     """
    #     try:
    #         Requirement.read(
    #             filePath=filePath
    #         )
    #         return ''
    #     except Exception as e:
    #         errorMsg = str(e)
    #         return errorMsg

    @staticmethod
    def is_ValidRequirementFile(
         filePath: Path
         ) -> bool:
        return Requirement.validateRequirementFile(filePath=filePath).valid

# -------------------------- EXPORT TOOLS -------------------------- #

    def toMD(self) -> str:

        listOfAttributes = self.attributesList

        # initiate MK object
        mk = MDText()

        # create title
        mk.add_title(self.title)

        # create paragraphs
        for attribute in listOfAttributes:
            if attribute != "title":
                mk.add_header(level=2, title=attribute.upper())
                mk.add_paragraph(text=getattr(self, attribute))
        return str(mk)

    def toMDFile(
            self,
            MDPath: Path
            ) -> Path:

        newMDFile = validateCorrectFileExtension(
            filePath=MDPath,
            validExtension=".md"
        )
        # write file
        with newMDFile.open("w+", encoding="utf-8") as f:
            f.write(self.toMD())

        return newMDFile

    @staticmethod
    def getMDFileName(reqpyfile: Path) -> str:
        return reqpyfile.stem 


class RequirementsSet(GenericDB):
    # ------------------------------ MODEL ----------------------------- #

    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(
            self,
            RequirementPath: Path):
        super().__init__(
            folderPath=RequirementPath,
            allowSubfolders=True,
            allowAdditionalFiles=True
        )

    # ----------------------------- FAKE DB ---------------------------- #

    def createFakeRequirementsSet(
            self,
            nfiles: int = 5,
            nfolders: int = 5,
            repeat: int = 4,
            maxdepth: int = 8,
            sigma_folders: int = 2,
            sigma_files: int = 1):

        alldirs = []
        allfiles = []
        basedir = self.folderPath
        for i in range(repeat):
            for root, dirs, files in os.walk(str(basedir)):
                for _ in range(int(random.gauss(nfolders, sigma_folders))):
                    p = Path(root) / random_string()
                    p.mkdir(exist_ok=True)
                    alldirs.append(p)
                for _ in range(int(random.gauss(nfiles, sigma_files))):
                    p = Path(root) / (
                        random_string() +
                        DEFAULT_REQPY_FILE_EXTENSION)
                    p = Requirement.writeFakeRequirementFile(p)
                    allfiles.append(p)
                depth = os.path.relpath(root, str(basedir)).count(os.sep)
                if maxdepth and depth >= maxdepth - 1:
                    del dirs[:]
        alldirs = list(set(alldirs))
        allfiles = list(set(allfiles))
        return alldirs, allfiles

    # ----------------------- DATABASE VALIDATION ---------------------- #
    def validateRequirementsDB(self) -> FileStatusList:

        # initiate
        out = FileStatusList([])

        # get list of MD File
        reqfiles = Directory(self.folderPath).list_valid_files(
            DEFAULT_REQPY_FILE_EXTENSION)

        # loop over all yaml files
        for reqfile in reqfiles:
            # Initiate a fileStatus for reqfile
            myfileStatus = FileStatus(
                filePath=reqfile,
                checks=CheckStatusList([]))

            # Requirement file validation
            myfileStatus.addCheckResult(
                result=Requirement.validateRequirementFile(
                    filePath=reqfile
                )
            )
            out.append(myfileStatus)
        return out
    
    # ----------------------- EXPORT TO MARKDOWN ----------------------- #
    def generateMD(
            self,
            targetDir: Path,
            show_console: bool = False
            ) -> None:

        Myconsole.apps(
            msg="Generate Markdown File for Requirements Folder",
            show_console=show_console
        )

        Myconsole.info(
            msg=f"Target folder : {targetDir.absolute()}",
            show_console=show_console
        )

        # validate database
        Myconsole.task(
                msg="Validate Requirement DataBase",
                show_console=show_console,
            )

        checks = self.validateRequirementsDB()

        if not checks.isAllFilesValid():
            Myconsole.error(
                msg=("The requirement database is not valid"
                     " - please see stack info"),
                show_console=show_console)
            raise ReqpyDBException("Requirement Data Base is invalid")

        Myconsole.ok(
            msg="Requirement Database is valid",
            show_console=show_console)

        # copy Folder structure and additional files
        self.copyFoldersFiles(
            destinationDir=targetDir,
            show_console=show_console)

        Myconsole.task(
                msg="Convert REQPY Files to Markdown files",
                show_console=show_console,
            )
        # list reqpy files
        listReqfiles = self.list_reqpy_files()

        Myconsole.info(
            msg=f"Number of files to convert : {len(listReqfiles)}",
            show_console=show_console
        )

        sequence = Myconsole.progressBar(
            sequence=listReqfiles,
            description="Generate Markdown files...",
            show_console=show_console
        )

        for reqfile in sequence:
            newFolder = (targetDir /
                         reqfile.relative_to(self.folderPath).parent)

            newFile = newFolder / (
                    Requirement.getMDFileName(reqfile) +
                    DEFAULT_REPORT_EXTENSION
                    )
            # write files

            newFile.parent.mkdir(parents=True, exist_ok=True)
            Requirement.read(reqfile).toMDFile(
                MDPath=newFile
            )
