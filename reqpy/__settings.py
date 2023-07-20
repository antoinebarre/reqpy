"""All settings needed by reqpy"""
# IMPORT MODULES
from typing import NamedTuple
import logging


# logger for logging
logger = logging.getLogger(__name__)

# ########################################################################## #
# ######################### REQUIREMENTS PARAMETERS ######################## #
# ########################################################################## #


class RequirementSettings(NamedTuple):
    min_title_length = 8  # min size of the title
    max_title_length = 60  # max size of the title
    max_description_length = 2000  # maximum size of the req description
    validation_status = ("VALID", "UNVALID", "INVALID")


DEFAULT_EXTENSION = ".yml"
DEFAULT_EXTENSION_REPORT = ".md"


class RequirementFileSettings(NamedTuple):
    allowed_extensions = [".yml", ".yaml"]  # allowed extensions
    default_extension = ".yml"  # default extension during file creation
