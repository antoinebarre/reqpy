"""Requirements management tools based on files (Yaml) and Python approach
"""

__app_name__ = "reqpy"
__version__ = "0.1.0"

import logging

from . import utils as utils
from . import requirements as requirements
from . import database as database
from . import folders as folders
from .tools import *
from .__logging import setup_logging, LogLevel


# logging format for reqpy
setup_logging(
    console_log_level=LogLevel.INFO,
    logfile_log_level=LogLevel.DEBUG
)
