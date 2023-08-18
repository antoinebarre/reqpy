from pathlib import Path
from typing import List, Union

from pydantic import BaseModel, ConfigDict, field_validator
from ..exception import ReqpyPathException

# =========================== PATH VALIDATION =========================== #


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
            validExtension: Union[str, List[str]],
            ) -> bool:
    """
    Check if the file extension of a Path is valid to write a requirement.

    Args:
        filePath (Path): The file path to validate.
        validExtension (Union[str, List[str]]): The allowed file extension(s).

    Returns:
        bool: True if the file extension is valid, False otherwise.

    Raises:
        TypeError: If validExtension is not a string or a list of strings.
        ValueError: If any extension in validExtension is not a string starting with a dot.

    """
    # convert to list for handling
    if isinstance(validExtension, str):
        validExtension = [validExtension]
    elif (
      isinstance(validExtension, list) and
      all(isinstance(item, str) for item in validExtension)):
        validExtension = validExtension
    else:
        raise TypeError(
            (
             "validExtension shall be a string or a list of string"
            )
        )
    # uppercase for the valid extensions
    uppercase_list = [string.upper() for string in validExtension]
    if (
      not all(string.startswith(".") for string in uppercase_list) or
      uppercase_list == []):
        raise ValueError(
            ("all exstention shall be a non empty string that starts with ."
             f"- Current: {uppercase_list}")
        )

    # get the file extension
    file_extension = filePath.suffix.upper()

    return file_extension in uppercase_list


def validateCorrectFileExtension(
            filePath: Path,
            validExtension: Union[str, List[str]],
            ) -> Path:
    """
    Validate the file extension of a Path against the allowed extension.

    Args:
        filePath (Path): The file path to validate.
        validExtension (str): The allowed file extension.

    Returns:
        Path: The input path if the extension is valid.

    Raises:
        ReqpyPathException: If the extension is not allowed.

    """

    if is_valid_file_extension(
             filePath,
             validExtension=validExtension):
        return filePath
    else:
        msg = (
            f"The file [{str(filePath.absolute())}] does not have  "
            "an allowed extension"
            f"  (i.e. {validExtension} )"
        )
        raise ReqpyPathException(msg)

# ========================== DIRECTORY ANALYSIS ========================= #


class Directory(BaseModel):
    # ------------------------------ MODEL ----------------------------- #
    dirPath: Path

    # ----------------------------- CONFIG ----------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # --------------------------- VALIDATION --------------------------- #

    @field_validator("dirPath")
    def dirPath_must_be_a_folder_existing_path(cls, dirPath: Path):
        """
        Validates that the dirPath attribute is an existing folder path.

        Args:
            cls: The class object.
            dirPath (Path): The root directory path to validate.

        Returns:
            Path: The validated root directory path.

        Raises:
            ValueError: If the rootdir attribute is not an
            existing folder path.
        """

        if not dirPath.is_dir():
            raise ReqpyPathException(
                "folderPath property shall be an existing folder path\n" +
                f" - Current dir (relative): {str(dirPath)}\n" +
                f" - Current dir (absolute): {str(dirPath.absolute())}\n"
            )
        return dirPath

    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(self, dirPath: Path):
        super().__init__(
            dirPath=dirPath,
        )

    # ----------------------------- LISTING ---------------------------- #

    def list_subdirectories(self) -> list[Path]:
        """
        List subdirectories of the directory as a list of Path objects.

        Args:
            None

        Returns:
            list[Path]: A list of Path objects representing the subdirectories.
        """
        subdirectories = [subdir for subdir in self.dirPath.iterdir()
                          if subdir.is_dir()]
        return subdirectories

    def list_all_files(
            self,
            ignoreFiles: list[str] = [],
            ) -> list[Path]:
        """
        List all files in a directory and its subdirectories
        except .gitignore files

        Args:
            directory_path (Path): The path to the directory.

        Returns:
            list[Path]: A list of Path objects representing the files.
        """
        files = []
        for file_path in self.dirPath.glob('**/*'):
            if (file_path.is_file() and
               file_path.name not in ignoreFiles):

                files.append(file_path)

        return files
    
    def list_invalid_files(
            self,
            validExtension : list[str]
            ) -> list[Path]:
        """
        List files in the directory and its subdirectories that have invalid
          extensions.

        Args:
            None

        Returns:
            list[Path]: A list of Path objects representing the files with
              invalid extensions.
        """
        return [filePath for filePath in self.list_all_files()
                if not has_appropriate_extension(filePath)]

    def list_valid_files(self) -> list[Path]:
        return [filePath for filePath in self.list_all_files()
                if has_appropriate_extension(filePath)]
