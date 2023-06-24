# import pytest
# from pathlib import Path
# from reqpy import ReqFolder
# from reqpy.__settings import FolderStructure
# import shutil

# # Test the ReqFolder class
# class TestReqFolder:
#     @pytest.fixture
#     def temp_folder(self, tmp_path_factory):
#         """
#         Fixture to create a temporary folder for testing.
#         """
#         temp_dir = tmp_path_factory.mktemp("req_folder")
#         yield temp_dir
#         shutil.rmtree(temp_dir)

#     def test_rootdir_must_be_a_folder_existing_path_valid(self, temp_folder):
#         """
#         Test that the rootdir validation passes for a valid existing folder path.
#         """
#         req_folder = ReqFolder(rootdir=temp_folder)
#         validated_path = req_folder.rootdir_must_be_a_folder_existing_path(req_folder.rootdir)
#         assert validated_path == temp_folder

#     def test_rootdir_must_be_a_folder_existing_path_invalid(self):
#         """
#         Test that a ValueError is raised when the rootdir validation fails for an invalid folder path.
#         """
#         invalid_folder_path = Path("nonexistent_folder")
        
#         with pytest.raises(ValueError):
#             req_folder = ReqFolder(rootdir=invalid_folder_path)
            

#     def test_create_dirs(self, temp_folder):
#         """
#         Test that the create_dirs() method successfully creates the directories defined in the FolderStructure.
#         """
#         req_folder = ReqFolder(rootdir=temp_folder)
#         req_folder.create_dirs()

#         # Check if the directories are created
#         for folder_name in FolderStructure.folder_structure:
#             folder_path = temp_folder / folder_name
#             assert folder_path.exists() == True


#     def test_clean_dirs(self, temp_folder):
#         """
#         Test that the clean_dirs() method removes the directories defined in the FolderStructure.
#         """
#         req_folder = ReqFolder(rootdir=temp_folder)
#         req_folder.create_dirs()

#         # Check if the directories exist before cleaning
#         for folder_name in FolderStructure.folder_structure:
#             folder_path = temp_folder / folder_name
#             assert folder_path.exists() == True
    
#         # Clean the directories
#         req_folder.clean_dirs()

#         # Check if the directories are removed
#         for folder_name in FolderStructure.folder_structure:
#             folder_path = temp_folder / folder_name
#             assert folder_path.exists() == False

import pytest
from pathlib import Path
from reqpy.__settings import FolderStructure, RequirementFileSettings
from reqpy.database import ReqFolder, DataBaseError
import shutil

@pytest.fixture
def req_folder(tmp_path):
    # Create a temporary directory for testing
    rootdir = tmp_path / "requirements"
    rootdir.mkdir()

    # Create the required folder structure
    for folder in FolderStructure.folder_structure:
        (rootdir / folder).mkdir()

    return ReqFolder(rootdir=rootdir)

def test_rootdir_must_be_a_folder_existing_path(req_folder):
    # Existing folder path should not raise an error
    assert ReqFolder(rootdir=req_folder.rootdir)

    # Non-existing folder path should raise a ValueError
    with pytest.raises(ValueError):
        ReqFolder(rootdir=req_folder.rootdir / "non_existing_folder")

def test_create_dirs(req_folder):
    req_folder.create_dirs()

    # Check if all the folders are created
    for folder in FolderStructure.folder_structure:
        assert (req_folder.rootdir / folder).is_dir()

def test_clean_dirs(req_folder):
    req_folder.clean_dirs()

    # Check if all the folders are deleted
    for folder in FolderStructure.folder_structure:
        assert not (req_folder.rootdir / folder).exists()

def test_get_missing_drectories(req_folder):
    missing_folders = req_folder.get_missing_drectories()

    # There should be no missing folders
    assert len(missing_folders) == 0

def test_get_list_of_files(req_folder):
    files = req_folder.get_list_of_files()

    # Since no files are added, the list should be empty
    assert len(files) == 0

def test_get_incorrect_files(req_folder):
    # Add some files with incorrect extensions
    incorrect_folder = req_folder.rootdir / FolderStructure.main_folder
    (incorrect_folder / "file1.txt").touch()
    (incorrect_folder / "file2.py").touch()

    incorrect_files = req_folder.get_incorrect_files()

    # Two files with incorrect extensions are added
    assert len(incorrect_files) == 2

def test_is_correct_files_false(req_folder):
    # Add some files with incorrect extensions
    incorrect_folder = req_folder.rootdir / FolderStructure.main_folder
    (incorrect_folder / "file1.txt").touch()
    (incorrect_folder / "file2.py").touch()

    assert not req_folder.is_correct_files()

def test_is_correct_files_true(req_folder):
    # Add some files with correct extensions
    correct_folder = req_folder.rootdir / FolderStructure.main_folder
    (correct_folder / "file1.yml").touch()
    (correct_folder / "file2.yml").touch()

    assert req_folder.is_correct_files()

def test_is_correct_folders(req_folder):
    # Remove one of the required folders
    shutil.rmtree(req_folder.rootdir / FolderStructure.folder_structure[0])

    assert not req_folder.is_correct_folders()

def test_get_list_of_files_with_missing_folders(req_folder):
    # Create a ReqFolder object without creating the required folders
    
    shutil.rmtree(req_folder.rootdir / "requirements")

    with pytest.raises(DataBaseError):
        req_folder.get_list_of_files()

