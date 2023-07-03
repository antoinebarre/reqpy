import pytest
import shutil
import tempfile
from pathlib import Path
from reqpy.folders import GenericFolder


@pytest.fixture
def temp_folder():
    # Create a temporary folder
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Clean up the temporary folder after the tests
    shutil.rmtree(temp_dir)


def test_has_appropriate_extension(temp_folder):
    # Create a test file with a valid extension
    file_path = temp_folder / "test_file.txt"
    file_path.touch()

    # Initialize the GenericFolder object
    folder = GenericFolder(temp_folder, allowedExtensions=[".txt"], allowSubfolders=True)

    # Test if the file has an appropriate extension
    assert folder.has_appropriate_extension(file_path)

    # Create a test file with an invalid extension
    file_path = temp_folder / "test_file.docx"
    file_path.touch()

    # Test if the file has an appropriate extension
    assert not folder.has_appropriate_extension(file_path)


def test_list_subdirectories(temp_folder):
    # Create subdirectories in the temporary folder
    subfolder1 = temp_folder / "subfolder1"
    subfolder1.mkdir()
    subfolder2 = temp_folder / "subfolder2"
    subfolder2.mkdir()

    # Initialize the GenericFolder object
    folder = GenericFolder(temp_folder, allowedExtensions=[], allowSubfolders=True)

    # Test if the subdirectories are listed correctly
    subdirectories = folder.list_subdirectories()
    assert len(subdirectories) == 2
    assert subfolder1 in subdirectories
    assert subfolder2 in subdirectories


def test_list_all_files(temp_folder):
    # Create files in the temporary folder and its subfolders
    file1 = temp_folder / "file1.txt"
    file1.touch()
    subfolder = temp_folder / "subfolder"
    subfolder.mkdir()
    file2 = subfolder / "file2.txt"
    file2.touch()

    # Initialize the GenericFolder object
    folder = GenericFolder(temp_folder, allowedExtensions=[".txt"], allowSubfolders=True)

    # Test if all files are listed correctly
    files = folder.list_all_files()
    assert len(files) == 2
    assert file1 in files
    assert file2 in files


def test_list_invalid_files(temp_folder):
    # Create files in the temporary folder with invalid extensions
    file1 = temp_folder / "file1.txt"
    file1.touch()
    file2 = temp_folder / "file2.docx"
    file2.touch()

    # Initialize the GenericFolder object
    folder = GenericFolder(temp_folder, allowedExtensions=[".txt"], allowSubfolders=True)

    # Test if invalid files are listed correctly
    invalid_files = folder.list_invalid_files()
    assert len(invalid_files) == 1
    assert file2 in invalid_files


def test_is_valid_folder_structure(temp_folder):
    # Initialize the GenericFolder object with subfolders allowed
    folder = GenericFolder(temp_folder, allowedExtensions=[], allowSubfolders=True)
    assert folder.is_valid_folder_structure()

    # Initialize the GenericFolder object with subfolders not allowed
    (temp_folder / "folder2").mkdir()
    folder = GenericFolder(temp_folder, allowedExtensions=[], allowSubfolders=False)
    assert not folder.is_valid_folder_structure()


def test_is_all_files_has_valid_extension(temp_folder):
    # Create files in the temporary folder with valid and invalid extensions
    file1 = temp_folder / "file1.txt"
    file1.touch()
    file2 = temp_folder / "file2.docx"
    file2.touch()

    # Initialize the GenericFolder object
    folder = GenericFolder(temp_folder, allowedExtensions=[".txt"], allowSubfolders=True)

    # Test if all files have valid extensions
    assert folder.is_all_files_has_valid_extension()

    # Change the allowed extensions to include ".docx"
    folder = GenericFolder(temp_folder, allowedExtensions=[".txt", ".docx"], allowSubfolders=True)

    # Test if not all files have valid extensions
    assert not folder.is_all_files_has_valid_extension()
