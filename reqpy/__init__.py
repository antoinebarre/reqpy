"""Requirements management tools based on files (Yaml) and Python approach
"""

__app_name__ = "reqpy"
__version__ = "0.1.0"


from loguru import logger
import sys

from .requirement import Requirement, RequirementsSet

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "{extra[ip]} {extra[user]} - <level>{message}</level>"
)
logger.configure(extra={"ip": "", "user": ""})  # Default values
logger.remove()
logger.add(sys.stderr, format=logger_format, level="WARNING")
logger.add("loguru.log", format=logger_format, level="TRACE", rotation="10 MB")

# Module import
