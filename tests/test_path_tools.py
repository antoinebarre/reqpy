import pytest
from pathlib import Path
from reqpy.exception import ReqpyPathException
from reqpy.tools.paths import validateFileExistence, validateFolderExistence, is_valid_file_extension, validateCorrectFileExtension
from typing import Union, List


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

def test_is_valid_file_extension_single_valid_extension():
    file_path = Path("test.txt")
    valid_extension = ".txt"
    assert is_valid_file_extension(file_path, valid_extension) is True

def test_is_valid_file_extension_single_invalid_extension():
    file_path = Path("test.jpg")
    valid_extension = ".txt"
    assert is_valid_file_extension(file_path, valid_extension) is False

def test_is_valid_file_extension_list_valid_extension():
    file_path = Path("test.txt")
    valid_extensions = [".txt", ".md"]
    assert is_valid_file_extension(file_path, valid_extensions) is True

def test_is_valid_file_extension_list_invalid_extension():
    file_path = Path("test.jpg")
    valid_extensions = [".txt", ".md"]
    assert is_valid_file_extension(file_path, valid_extensions) is False

def test_is_valid_file_extension_case_insensitive_valid_extension():
    file_path = Path("test.TXT")
    valid_extension = ".txt"
    assert is_valid_file_extension(file_path, valid_extension) is True

def test_is_valid_file_extension_case_insensitive_invalid_extension():
    file_path = Path("test.JPG")
    valid_extension = ".txt"
    assert is_valid_file_extension(file_path, valid_extension) is False

def test_is_valid_file_extension_multiple_valid_extensions():
    file_path = Path("test.md")
    valid_extensions = [".txt", ".md"]
    assert is_valid_file_extension(file_path, valid_extensions) is True

def test_is_valid_file_extension_invalid_validExtension_type():
    file_path = Path("test.txt")
    invalid_valid_extension = 123
    with pytest.raises(TypeError):
        is_valid_file_extension(file_path, invalid_valid_extension)

def test_is_valid_file_extension_empty_validExtension_list():
    file_path = Path("test.txt")
    empty_valid_extensions = []
    with pytest.raises(ValueError):
        is_valid_file_extension(file_path, empty_valid_extensions)

def test_is_valid_file_extension_invalid_extension_format():
    file_path = Path("test.txt")
    invalid_extensions = [".txt", "md"]
    with pytest.raises(ValueError):
        is_valid_file_extension(file_path, invalid_extensions)

def test_validateCorrectFileExtension_valid_extension():
    file_path = Path("test.txt")
    valid_extension = ".txt"
    result = validateCorrectFileExtension(file_path, valid_extension)
    assert result == file_path

def test_validateCorrectFileExtension_invalid_extension():
    file_path = Path("test.jpg")
    valid_extension = ".txt"
    with pytest.raises(ReqpyPathException):
        validateCorrectFileExtension(file_path, valid_extension)