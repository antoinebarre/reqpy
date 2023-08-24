""" Definition tools for reqpy"""

# IMPORT SECTION
from __future__ import annotations
from .definitionItems import DefintionType

from .requirementItems import ValidationStatus
from .settings import RequirementSettings

from .__genericItem import GenericItem

from pydantic import BaseModel, ConfigDict, Field


class Definition(BaseModel, GenericItem):

    # ------------------------------- MODELS ------------------------- #
    title: str
    description: str = Field(
        default="Description or meaning of the Definition as Markdown"
    )
    comment: str = Field(
        default=(
            "Comment of the Definition - no use for acronyms"
            )
    )
    synonyms: list[str] = Field(
                                default=[""])
    definition_type: DefintionType = DefintionType.DEFINITION
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
            definition_type: DefintionType = DefintionType.DEFINITION,
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