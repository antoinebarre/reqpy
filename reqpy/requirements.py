""" Requirements class definition of reqpy and associated tools"""

# IMPORT SECTION
from enum import auto, StrEnum
from datetime import datetime
from pydantic import BaseModel, Field, validator
from .__settings import RequirementSettings


# ########################################################################## #
# ############################### UTILS CLASS ############################## #
# ########################################################################## #
class ValidationStatus(StrEnum):
    """
    Enumeration representing the validation status of a requirement.

    Attributes:
        VALID: The requirement is valid.
        UNVALID: The requirement is not yet validated.
        INVALID: The requirement is invalid.

    """
    VALID = auto()
    UNVALID = auto()
    INVALID = auto()

# ########################################################################## #
# ############################ REQUIREMENT CLASS ########################### #
# ########################################################################## #

class Requirement(BaseModel):
    """
    Represents a requirement with title, content, validation status, and creation date.

    Attributes:
        title (str): The title of the requirement.
        content (str): The content of the requirement.
        validation_status (ValidationStatus): The validation status of the requirement.
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
    validation_status: ValidationStatus = ValidationStatus.UNVALID
    creation_date: datetime = datetime.now()

    @validator('title')
    def title_must_start_with_alpha(cls, title: str):
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
            raise ValueError('First character shall be an alphabet (a-z or A-Z).')
        return title.capitalize()

    # -------------------------- #
    class Config:
        """Configuration class for the Requirement class.
        """
        allow_mutation = True  # allow mutation for the class Requirement
        validate_assignment = True # activate the validation for assignement
