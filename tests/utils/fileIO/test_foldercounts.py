import pytest
import pathlib
from reqpy.utils.fileIO import count_folders 


@pytest.fixture(scope="function")
def temp_folders(tmp_path) -> pathlib.Path:
    # Create temporary folders for testing
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()

    subfolder1 = folder_path / "subfolder1"
    subfolder1.mkdir()

    subfolder2 = folder_path / "subfolder2"
    subfolder2.mkdir()

    subfolder3 = folder_path / "__dunder_folder__"
    subfolder3.mkdir()

    hidden_folder = folder_path / ".hidden_folder"
    hidden_folder.mkdir()

    subsubfolder1 = subfolder1 / "sub1"
    subsubfolder1.mkdir()
    subsubfolder2 = subfolder1 / "sub2"
    subsubfolder2.mkdir()

    subsubfhidden = subfolder1 / ".hidden_folder"
    subsubfhidden.mkdir()
    subdunder = subfolder1 / "__dunder_folder__"
    subdunder.mkdir()
    

    return folder_path


def test_count_folders(temp_folders):
    """
    Test case to ensure that count_folders correctly counts the number of folders.
    """

    folder_path = temp_folders

    # Call the function under test
    result = count_folders(folder_path)

    # Perform assertions
    assert result == 4


def test_count_folders_with_include_subfolders(temp_folders):
    """
    Test case to ensure that count_folders correctly counts the number of folders with include_subfolders=True.
    """

    folder_path = temp_folders

    # Call the function under test with include_subfolders=True
    result = count_folders(folder_path, include_subfolders=True)

    # Perform assertions
    assert result == 8


def test_count_folders_with_exclude_dunder_folders(temp_folders):
    """
    Test case to ensure that count_folders correctly counts the number of folders with exclude_dunder_folders=True.
    """

    folder_path = temp_folders

    # Call the function under test with exclude_dunder_folders=True
    result = count_folders(folder_path, exclude_dunder_folders=True)

    # Perform assertions
    assert result == 3


def test_count_folders_with_exclude_hidden_folders(temp_folders):
    """
    Test case to ensure that count_folders correctly counts the number of folders with exclude_hidden_folders=True.
    """

    folder_path = temp_folders

    # Call the function under test with exclude_hidden_folders=True
    result = count_folders(folder_path, exclude_hidden_folders=True)

    # Perform assertions
    assert result == 3


def test_count_folders_with_all_options(temp_folders):
    """
    Test case to ensure that count_folders correctly counts the number of folders with all options enabled.
    """

    folder_path = temp_folders

    # Call the function under test with all options enabled
    result = count_folders(folder_path, include_subfolders=True, exclude_dunder_folders=True, exclude_hidden_folders=True)

    # Perform assertions
    assert result == 4
