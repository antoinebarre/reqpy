import pathlib
from reqpy.requirements import Requirement
from reqpy.database import ReqFolder
from reqpy.__settings import FolderStructure
from reqpy.utils import generate_random_string, randomText
from faker import Faker
from reqpy.demo import generate_DB


def test_generate_DB():
    """
    Test case to ensure that the generate_DB function creates the requirement database correctly.
    """

    # Set up test data
    nbFilesPerFolder = 2
    nbFolder = 2
    path = pathlib.Path("test_path")
    path.mkdir(exist_ok=True)

    # Call the function under test
    generate_DB(nbFilesPerFolder, nbFolder, path)

    # Perform assertions
    reqF = ReqFolder(rootdir=path)

    # Check if the root directory and subdirectories exist
    assert (path / FolderStructure.main_folder).exists()
    assert (path / FolderStructure.main_folder / "folder1").exists()
    assert (path / FolderStructure.main_folder / "folder2").exists()

    # Check if the correct number of files are created in each folder
    folder1_files = list((path / FolderStructure.main_folder / "folder1").iterdir())
    assert len(folder1_files) == nbFilesPerFolder

    folder2_files = list((path / FolderStructure.main_folder / "folder2").iterdir())
    assert len(folder2_files) == nbFilesPerFolder

    # Check if each file is a valid Requirement object
    for file_path in folder1_files:
        req = Requirement.read(file_path)
        assert isinstance(req, Requirement)

    for file_path in folder2_files:
        req = Requirement.read(file_path)
        assert isinstance(req, Requirement)

    # Clean up the test data
    reqF.clean_dirs()


def test_generate_DB_with_default_values():
    """
    Test case to ensure that the generate_DB function works correctly with default parameter values.
    """

    # Set up test data
    path = pathlib.Path("test_path")

    # Call the function under test with default values
    generate_DB(path=path)

    # Perform assertions
    reqF = ReqFolder(rootdir=path)

    # Check if the root directory and subdirectories exist
    assert (path / FolderStructure.main_folder).exists()

    # Clean up the test data
    reqF.clean_dirs()
