""" 
======================== UNIT TEST FILE LISTING =======================
"""

import reqpy
import os

import pytest
import pathlib
from reqpy.utils.fileIO import list_files

def test_listdirectory():
    
    try:
        reqpy.utils.fileIO.listdirectory(os.getcwd(),extensions=".py",excluded_folders=("venv",".git"))
    except:
        assert False



@pytest.fixture
def create_test_files(tmp_path):
    # Create test files in the temporary directory
    file1 = tmp_path / "file1.txt"
    file1.write_text("Test file 1")
    file2 = tmp_path / "folder1" / "file2.txt"
    file2.parent.mkdir()
    file2.write_text("Test file 2")
    file3 = tmp_path / "__folder2" / "file3.txt"
    file3.parent.mkdir()
    file3.write_text("Test file 3")
    file4 = tmp_path / ".hidden_folder" / "file4.txt"
    file4.parent.mkdir()
    file4.write_text("Test file 4")
    
    
    return {
        "root_dir": tmp_path,
        "default_result": [
        file1,
        ],
        "default_result_including_subfolder": [
        file1,
        file2,
        file3,
        file4
        ],
        "default_result_excluding_dunder": [
        file1,
        file2,
        file4
        ],
        "default_result_excluding_hidden": [
        file1,
        file2,
        file3,
        ],
        "result_all_option": [
        file1,
        file2,
        ],

    }



def test_list_files_without_options(create_test_files):
    
    folder_path = create_test_files["root_dir"]
    files = list_files(folder_path)
    
    case_name = "default_result"
    
    assert len(files) == len(create_test_files[case_name])
    assert all(filepath in create_test_files[case_name] for filepath in files)


def test_list_files_include_subfolders(create_test_files):
       
    folder_path = create_test_files["root_dir"]
    files = list_files(folder_path, include_subfolders=True)
    
    case_name = "default_result_including_subfolder"
    
    assert len(files) == len(create_test_files[case_name])
    assert all(filepath in create_test_files[case_name] for filepath in files)



def test_list_files_exclude_dunder_folders(create_test_files):
      
    folder_path = create_test_files["root_dir"]
    files = list_files(folder_path, exclude_dunder_folders=True,include_subfolders=True)
    
    case_name = "default_result_excluding_dunder"
    
    assert len(files) == len(create_test_files[case_name])
    assert all(filepath in create_test_files[case_name] for filepath in files)


def test_list_files_exclude_hidden_folders(create_test_files):
    folder_path = create_test_files["root_dir"]
    files = list_files(folder_path, exclude_hidden_folders=True,include_subfolders=True)
    
    case_name = "default_result_excluding_hidden"
    
    assert len(files) == len(create_test_files[case_name])
    assert all(filepath in create_test_files[case_name] for filepath in files)



def test_list_files_with_all_options(create_test_files):
    folder_path = create_test_files["root_dir"]
    files = list_files(folder_path, exclude_hidden_folders=True,include_subfolders=True,exclude_dunder_folders=True)
    
    case_name = "result_all_option"
    
    assert len(files) == len(create_test_files[case_name])
    assert all(filepath in create_test_files[case_name] for filepath in files)


def test_list_files_with_nonexistent_folder():
    folder_path = pathlib.Path("/path/to/nonexistent/folder")
    with pytest.raises(FileExistsError):
        list_files(folder_path)
