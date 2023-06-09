import pytest
from pathlib import Path
from reqpy import ReqFolder
from reqpy.__settings import FolderStructure
import shutil

# Test the ReqFolder class
class TestReqFolder:
    @pytest.fixture
    def temp_folder(self, tmp_path_factory):
        """
        Fixture to create a temporary folder for testing.
        """
        temp_dir = tmp_path_factory.mktemp("req_folder")
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_rootdir_must_be_a_folder_existing_path_valid(self, temp_folder):
        """
        Test that the rootdir validation passes for a valid existing folder path.
        """
        req_folder = ReqFolder(rootdir=temp_folder)
        validated_path = req_folder.rootdir_must_be_a_folder_existing_path(req_folder.rootdir)
        assert validated_path == temp_folder

    def test_rootdir_must_be_a_folder_existing_path_invalid(self):
        """
        Test that a ValueError is raised when the rootdir validation fails for an invalid folder path.
        """
        invalid_folder_path = Path("nonexistent_folder")
        
        with pytest.raises(ValueError):
            req_folder = ReqFolder(rootdir=invalid_folder_path)
            

    def test_create_dirs(self, temp_folder):
        """
        Test that the create_dirs() method successfully creates the directories defined in the FolderStructure.
        """
        req_folder = ReqFolder(rootdir=temp_folder)
        req_folder.create_dirs()

        # Check if the directories are created
        for folder_name in FolderStructure.folder_structure:
            folder_path = temp_folder / folder_name
            assert folder_path.exists() == True


    def test_clean_dirs(self, temp_folder):
        """
        Test that the clean_dirs() method removes the directories defined in the FolderStructure.
        """
        req_folder = ReqFolder(rootdir=temp_folder)
        req_folder.create_dirs()

        # Check if the directories exist before cleaning
        for folder_name in FolderStructure.folder_structure:
            folder_path = temp_folder / folder_name
            assert folder_path.exists() == True
    
        # Clean the directories
        req_folder.clean_dirs()

        # Check if the directories are removed
        for folder_name in FolderStructure.folder_structure:
            folder_path = temp_folder / folder_name
            assert folder_path.exists() == False
