import pytest
import pathlib
from reqpy.utils.fileIO import list_folders


@pytest.fixture
def setup_folders(tmp_path):
    """
    Fixture to set up folders for testing.
    """
    folder_path :pathlib.Path = tmp_path / "test_folder"
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

    return {
        "root_dir": folder_path,
        "default_result": [
        subfolder1,
        subfolder2,
        subfolder3,
        hidden_folder
        ],
        "default_result_including_subfolder": [
        subfolder1,
        subfolder2,
        subfolder3,
        hidden_folder,
        subsubfolder1,
        subsubfolder2,
        subsubfhidden,
        subdunder,
        ],
        "default_result_excluding_dunder": [
        subfolder1,
        subfolder2,
        hidden_folder
        ],
        "default_result_excluding_hidden": [
        subfolder1,
        subfolder2,
        subfolder3,
        ],
        "result_all_option": [
        subfolder1,
        subfolder2,
        subsubfolder1,
        subsubfolder2,
        ],

    }


def test_list_containing_folders(setup_folders):
    """
    Test case to ensure that the list_containing_folders function lists the containing folders correctly.
    """

    root_folder = setup_folders["root_dir"]

    # Call the function under test
    containing_folders = list_folders(root_folder)

    # Perform assertions
    assert len(containing_folders) == len(setup_folders["default_result"])
    assert all(folder in setup_folders["default_result"] for folder in containing_folders)


def test_list_containing_folders_with_include_subfolders(setup_folders):
    """
    Test case to ensure that the list_containing_folders function lists the containing folders correctly with include_subfolders option.
    """

    root_folder = setup_folders["root_dir"]

    # Call the function under test
    containing_folders = list_folders(root_folder,include_subfolders=True)

    # Perform assertions
    assert len(containing_folders) == len(setup_folders["default_result_including_subfolder"])
    assert all(folder in setup_folders["default_result_including_subfolder"] for folder in containing_folders)


def test_list_containing_folders_with_exclude_dunder_folders(setup_folders):
    """
    Test case to ensure that the list_containing_folders function lists the containing folders correctly with exclude_dunder_folders option.
    """

    root_folder = setup_folders["root_dir"]

    # Call the function under test
    containing_folders = list_folders(root_folder,exclude_dunder_folders=True)

    # Perform assertions
    assert len(containing_folders) == len(setup_folders["default_result_excluding_dunder"])
    assert all(folder in setup_folders["default_result_excluding_dunder"] for folder in containing_folders)


def test_list_containing_folders_with_exclude_hidden_folders(setup_folders):
    """
    Test case to ensure that the list_containing_folders function lists the containing folders correctly with exclude_hidden_folders option.
    """

    root_folder = setup_folders["root_dir"]

    # Call the function under test
    containing_folders = list_folders(root_folder,exclude_hidden_folders=True)

    # Perform assertions
    assert len(containing_folders) == len(setup_folders["default_result_excluding_hidden"])
    assert all(folder in setup_folders["default_result_excluding_hidden"] for folder in containing_folders)


def test_list_containing_folders_with_all_options(setup_folders):
    """
    Test case to ensure that the list_containing_folders function lists the containing folders correctly with all options.
    """

    root_folder = setup_folders["root_dir"]

    # Call the function under test with all options set to True
    containing_folders = list_folders(
        root_folder,
        include_subfolders=True,
        exclude_dunder_folders=True,
        exclude_hidden_folders=True
    )


    # Perform assertions
    assert len(containing_folders) == len(setup_folders["result_all_option"])
    assert all(folder in setup_folders["result_all_option"] for folder in containing_folders)

