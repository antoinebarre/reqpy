from pathlib import Path
from ..exception import ReqpyPathException


def validateFileExistence(path: Path) -> Path:
    """validate if a file defined by a Path exists if yes
    return the path else raise an exception"""

    if path.is_file():
        return path
    else:
        msg = f"The file {path.absolute()} does not exist"
        raise ReqpyPathException(msg)


def validateFolderExistence(path: Path) -> Path:
    """validate if a folder defined by a Path exists if yes
    return the path else raise an exception"""

    if path.is_dir():
        return path
    else:
        msg = f"The folder {path.absolute()} does not exist"
        raise ReqpyPathException(msg)

 
def is_valid_file_extension(
            filePath: Path,
            allowedExtension: str,
            ) -> bool:
    """
    Check if the file extension of a Path is valid to write a requirement.

    Args:
        filePath (Path): The file path to validate.

    Returns:
        bool: True if the file extension is valid, False otherwise.

    """
    # get file extension
    file_extension = filePath.suffix

    return (file_extension == allowedExtension)

# TODO : allow a list of extensions


def validateCorrectFileExtension(
            filePath: Path,
            allowedExtension: str,
            ) -> Path:

    if is_valid_file_extension(
             filePath,
             allowedExtension=allowedExtension):
        return filePath
    else:
        msg = (
            f"The file [{str(filePath.absolute())}] does not have  "
            "an allowed extension"
            f"  (i.e. {allowedExtension} )"
        )
        raise ReqpyPathException(msg)
