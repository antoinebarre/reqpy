""" Package with Hig level function of the reqpy package """

from pathlib import Path
from reqpy.database import ReqFolder
import logging
from typing import Any, Callable
import functools

__all__ = [
    "init_reqpy",
    "reset_reqpy"
]


# logging wrapper
def with_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logging.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__}")
        return value

    return wrapper


@with_logging
def reset_reqpy(
 folder: Path = Path()
 ) -> None:
    try:
        logging.debug(
            f"The path provided is {str(folder)} [type: {type(folder)}]"
            )
        t = ReqFolder(rootdir=folder)

        # create the folder:
        t.clean_dirs()

    except Exception:
        logging.exception(
            "Exception occurred during the requirement project initialization"
            )


@with_logging
def init_reqpy(folder: Path = Path()) -> None:
    """
    Initialize the reqpy requirement project.

    Args:
        folder (Path, optional): The root folder path. Defaults to Path().

    Returns:
        None

    Raises:
        Exception: If an exception occurs during the requirement
          project initialization.
    """
    try:
        logging.debug(
            f"The path provided is {str(folder)} [type: {type(folder)}]"
            )
        t = ReqFolder(rootdir=folder)

        # create the folder:
        t.create_dirs()

    except Exception:
        logging.exception(
            "Exception occurred during the requirement project initialization"
            )
