import pytest
import shutil
from pathlib import Path
from reqpy.dirSkeleton import FolderStructure


def test_FolderStructure_with_nonexisting_path(tmp_path):
    with pytest.raises(FileExistsError):
        FolderStructure(currentFolderPath=Path("toto"))

def test_FolderStructure_create_and_delete_folders(tmp_path):
    folder_structure = FolderStructure(currentFolderPath=tmp_path)

    # Check that all folders do not exist
    assert not folder_structure.all_folders_exist()

    # create folder
    folder_structure.create_folders()

    # Check that all folders exist
    assert folder_structure.all_folders_exist() 

    # Delete folders
    folder_structure.delete_folders()

    # Check that all folders are deleted
    assert not folder_structure.all_folders_exist()

def test_FolderStructure_reset_folders(tmp_path):
    folder_structure = FolderStructure(currentFolderPath=tmp_path)
    folder_structure.create_folders()
    # Check that all folders exist
    assert folder_structure.all_folders_exist()

    # Reset folders
    folder_structure.reset_folders()

    # Check that all folders exist again after resetting
    assert folder_structure.all_folders_exist()

def test_FolderStructure_create_gitignore_file(tmp_path):
    folder_structure = FolderStructure(currentFolderPath=tmp_path)

    # create folders
    folder_structure.create_folders()
    main_folder = folder_structure.main_folder
    gitignore_path = FolderStructure.create_gitignore_file(main_folder)

    assert gitignore_path.is_file()
    assert gitignore_path.read_text() == "# Add your gitignore rules here"


def test_FolderStructure_foldersList(tmp_path):
    folder_structure = FolderStructure(currentFolderPath=tmp_path)

    folder_structure.create_folders()

    # Check the folders list
    folders_list = folder_structure.foldersList

    # Ensure that the list is not empty
    assert folders_list

    # Ensure that each folder in the list exists
    for folder in folders_list:
        assert folder.exists()

def test_FolderStructure_get_missing_folders(tmp_path):
    folder_structure = FolderStructure(currentFolderPath=tmp_path)

    folder_structure.create_folders()

    # Check the list of missing folders (should be empty initially)
    missing_folders = folder_structure.get_missing_folders()
    assert not missing_folders

    # Delete one of the folders
    deleted_folder = folder_structure.requirements_folder
    shutil.rmtree(deleted_folder)

    # Check the list of missing folders again (should have the deleted folder)
    missing_folders = folder_structure.get_missing_folders()
    assert deleted_folder in missing_folders

def test_FolderStructure_all_folders_exist(tmp_path):
    folder_structure = FolderStructure(currentFolderPath=tmp_path)

    folder_structure.create_folders()

    # Check that all folders exist initially
    assert folder_structure.all_folders_exist()

    # Delete one of the folders
    deleted_folder = folder_structure.definition_folder
    shutil.rmtree(deleted_folder)

    # Check that not all folders exist after deleting one
    assert not folder_structure.all_folders_exist()

