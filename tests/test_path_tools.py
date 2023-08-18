import pytest
from pathlib import Path
from reqpy.exception import ReqpyPathException
from reqpy.tools.paths import validateFileExistence, validateFolderExistence, is_valid_file_extension, validateCorrectFileExtension

def test_validateFileExistence_existing_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.touch()
    assert validateFileExistence(file_path) == file_path

def test_validateFileExistence_nonexistent_file(tmp_path):
    file_path = tmp_path / "nonexistent_file.txt"
    with pytest.raises(ReqpyPathException):
        validateFileExistence(file_path)

def test_validateFolderExistence_existing_folder(tmp_path):
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()
    assert validateFolderExistence(folder_path) == folder_path

def test_validateFolderExistence_nonexistent_folder(tmp_path):
    folder_path = tmp_path / "nonexistent_folder"
    with pytest.raises(ReqpyPathException):
        validateFolderExistence(folder_path)

def test_is_valid_file_extension_valid_extension():
    file_path = Path("test.txt")
    allowed_extension = ".txt"
    assert is_valid_file_extension(file_path, allowed_extension) is True

def test_is_valid_file_extension_invalid_extension():
    file_path = Path("test.jpg")
    allowed_extension = ".txt"
    assert is_valid_file_extension(file_path, allowed_extension) is False

def test_validateCorrectFileExtension_valid_extension(tmp_path):
    file_path = tmp_path / "test.txt"
    allowed_extension = ".txt"
    assert validateCorrectFileExtension(file_path, allowed_extension) == file_path

def test_validateCorrectFileExtension_invalid_extension(tmp_path):
    file_path = tmp_path / "test.jpg"
    allowed_extension = ".txt"
    with pytest.raises(ReqpyPathException):
        validateCorrectFileExtension(file_path, allowed_extension)
