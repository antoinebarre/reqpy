""" Definition tools for reqpy"""

# IMPORT SECTION
from __future__ import annotations
from pathlib import Path
from typing import Callable

from reqpy.constants import DEFAULT_REQPY_FILE_EXTENSION
from reqpy.tools.image import generate_random_image
from reqpy.tools.status import CheckStatus, CheckStatusList
from reqpy.tools.strings import generate_paragraph, random_Title

from .exception import ReqpyIOException
from .definitionItems import DefinitionType

from .requirementItems import ValidationStatus
from .settings import DefinitionSettings

from .__genericItem import GenericItem
from .__logging import log

from pydantic import BaseModel, ConfigDict, Field


class Definition(BaseModel, GenericItem):

    # ------------------------------- MODELS ------------------------- #
    title: str = Field(
        min_length=DefinitionSettings.min_title_length,
        max_length=DefinitionSettings.max_description_length)
    description: str = Field(
        max_length=DefinitionSettings.max_description_length,
        default="Description or meaning of the Definition as Markdown"
    )
    comment: str = Field(
        default=(
            "Comment of the Definition - not used for acronyms"
            )
    )
    synonyms: list[str] = Field(
                                default=[""])
    definition_type: DefinitionType = DefinitionType.DEFINITION
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
            description: str = "Definition as Markdown",
            comment: str = "Comment of the Definition - no use for acronyms",
            synonyms: list[str] = [""],
            definition_type: DefinitionType = DefinitionType.DEFINITION,
            validation_status: ValidationStatus = ValidationStatus.UNVALID,
            **kwargs
            ):

        super().__init__(
            title=title,
            description=description,
            comment=comment,
            synonyms=synonyms,
            definition_type=definition_type,
            validation_status=validation_status,
            **kwargs
        )

    # ------------------------- DUNDER METHODS ------------------------- #
    def __str__(self):
        return GenericItem.__str__(self)

    # -------------------------- READ / WRITE TOOLS ------------------------- #

    @staticmethod
    def read(
            filePath: Path,
            ) -> Definition:

        data = Definition.read2dict(
            filePath=filePath)

        # logging
        log.trace(
            (f"readed dict: \n{data}"))
        try:
            new_def = Definition(**data)

        except Exception as e:
            raise ReqpyIOException(
                f"Impossible to parse the YAML file {filePath}" +
                f" due to this error: \n{str(e)}"
            )
        return new_def

    @staticmethod
    def create_new_definition(
        filePath: Path,
            ) -> Path:
        # new requirement
        definition = Definition(title="New Definition to rename")
        # analyze file name
        fileName = filePath.stem
        dir_path = filePath.parent

        try:
            file_number = 1
            while True:
                file_name = f"{fileName}{file_number:02d}"
                file_path = (dir_path /
                             (file_name + DEFAULT_REQPY_FILE_EXTENSION))
                if not file_path.exists():
                    definition.write(filePath=file_path)

                    # logging
                    log.trace(
                        f"new definition file created: {file_path.absolute()} "
                    )
                    return file_path
                file_number += 1
        except Exception as e:
            raise RuntimeError("An error occurred:", str(e))

    # ------------------------ FAKE REQUIREMENT ------------------------ #
    @staticmethod
    def createFakeDefinition() -> Definition:
        return Definition(
            title=random_Title(
                min_length=DefinitionSettings.min_title_length,
                max_length=DefinitionSettings.max_title_length
                ),
            description=generate_paragraph(
                max_characters=DefinitionSettings.max_description_length
            ),
            rationale=generate_paragraph(
                max_characters=DefinitionSettings.max_description_length
            )
        )

    @staticmethod
    def writeFakeRequirementFile_withPictures(
            filePath: Path,
            ) -> Path:

        # create fake Requirement
        definition = Definition.createFakeDefinition()

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
        definition.description += f"\n[IMG TEST 01]({imgPath1.name})\n"
        definition.comment += f"\n[IMG TEST 02]({imgPath2.name})\n"

        # write file
        filePath = definition.write(
            filePath=filePath,
            )
        return filePath

    @staticmethod
    def writeFakeRequirementFile(
            filePath: Path,
            ) -> Path:

        # create fake Requirement
        definition = Definition.createFakeDefinition()

        # write file
        filePath = definition.write(
            filePath=filePath,
            )
        return filePath

    # -------------------------- EXPORT TOOLS -------------------------- #

    def get_all_occurences(self) -> list[str]:

        list_of_occurences = [self.title]

        # add synonyms
        list_of_occurences.extend(self.synonyms)

        # remove empty strings
        while ("" in list_of_occurences):
            list_of_occurences.remove("")

        # remove duplicates
        list_of_occurences = list(dict.fromkeys(list_of_occurences))

        return list_of_occurences

    # ------------------------ VALIDATION TOOLS ------------------------ #
    @staticmethod
    def validateDefinitionFile(
            filePath: Path
            ) -> CheckStatusList:

        # list of checks
        check_list_fct: list[Callable] = [
            Definition.__validate_filename_definition_file,
            Definition.__validate_reading_definition_file,
        ]

        out = [check(filePath) for check in check_list_fct]

        return CheckStatusList(out)

    @staticmethod
    def __validate_reading_definition_file(
         filePath: Path
         ) -> CheckStatus:

        checkName = "Validate the read of the Definition file"

        try:
            Definition.read(
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

    @staticmethod
    def __validate_filename_definition_file(
         filePath: Path
         ) -> CheckStatus:

        checkName = (
            "Validate if the name is the same"
            " of the title with space replace by _"
            )

        try:
            def1 = Definition.read(
                filePath=filePath
            )

            # replace title name
            expected_filename = def1.title.replace(" ", "_")

            if expected_filename == filePath.stem:
                return CheckStatus.createValid(checkName=checkName)
            else:
                errorMsg = (
                    f"File Name should be {expected_filename}"
                    f" - Current : {filePath.stem}")
                return CheckStatus(
                    checkName=checkName,
                    valid=False,
                    message=errorMsg
                    )

        except Exception as e:
            errorMsg = str(e)
            return CheckStatus(
                checkName="Impossible to execute : " + checkName,
                valid=False,
                message=errorMsg
            )

    @staticmethod
    def is_ValidRequirementFile(
         filePath: Path
         ) -> bool:
        return Definition.validateDefinitionFile(filePath=filePath).is_valid()
