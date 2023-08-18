from pathlib import Path
from ..exception import ReqpyPathException


def validateFileExistence(path: Path) -> Path:
    """
    Validate if a file defined by a Path exists; if yes,
    return the path, otherwise raise an exception.

    Args:
        path (Path): The file path to validate.

    Returns:
        Path: The input path if it is an existing file.

    Raises:
        ReqpyPathException: If the file does not exist.

    """

    if path.is_file():
        return path
    else:
        msg = f"The file {path.absolute()} does not exist"
        raise ReqpyPathException(msg)


def validateFolderExistence(path: Path) -> Path:
    """
    Validate if a folder defined by a Path exists; if yes,
    return the path, otherwise raise an exception.

    Args:
        path (Path): The folder path to validate.

    Returns:
        Path: The input path if it is an existing folder.

    Raises:
        ReqpyPathException: If the folder does not exist.

    """

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
        allowedExtension (str): The allowed file extension.

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
    """
    Validate the file extension of a Path against the allowed extension.

    Args:
        filePath (Path): The file path to validate.
        allowedExtension (str): The allowed file extension.

    Returns:
        Path: The input path if the extension is valid.

    Raises:
        ReqpyPathException: If the extension is not allowed.

    """

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
