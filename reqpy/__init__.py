"""Requirements management tools based on files (Yaml) and Python approach
"""

__app_name__ = "reqpy"
__version__ = "0.1.0"

import logging

from . import utils as utils
from . import requirements as requirements
from . import database as database
from .tools import *


# logging format for reqpy
logging.basicConfig(
    format='%(asctime)s %(funcName)20s %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.WARNING
    )