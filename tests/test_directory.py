from pathlib import Path
import pytest
from reqpy.tools.paths import Directory
from reqpy.exception import ReqpyPathException


@pytest.fixture
def temp_dir(tmp_path) -> Path:
    return tmp_path

def test_Directory_init(temp_dir: Path):
    dir_path = temp_dir / "test_dir"
    dir_path.mkdir()
    directory = Directory(dirPath=dir_path)
    assert directory.dirPath == dir_path

def test_Directory_dirPath_must_be_a_folder_existing_path(temp_dir: Path):
    dir_path = temp_dir / "test_file.txt"
    dir_path.touch()
    with pytest.raises(ReqpyPathException):
        Directory(dirPath=dir_path)

def test_Directory_list_subdirectories(temp_dir: Path):
    parent_dir = temp_dir / "parent_dir"
    parent_dir.mkdir()
    subdir1 = parent_dir / "subdir1"
    subdir1.mkdir()
    subdir2 = parent_dir / "subdir2"
    subdir2.mkdir()

    directory = Directory(dirPath=parent_dir)
    subdirectories = directory.list_subdirectories()
    
    assert subdir1 in subdirectories
    assert subdir2 in subdirectories

def test_Directory_list_all_files(temp_dir: Path):
    parent_dir = temp_dir / "parent_dir"
    parent_dir.mkdir()
    file1 = parent_dir / "file1.txt"
    file1.touch()
    file2 = parent_dir / "file2.txt"
    file2.touch()
    subdir = parent_dir / "subdir"
    subdir.mkdir()
    file3 = subdir / "file3.txt"
    file3.touch()

    directory = Directory(dirPath=parent_dir)
    files = directory.list_all_files()

    assert file1 in files
    assert file2 in files
    assert file3 in files

def test_Directory_list_all_files_with_ignore(temp_dir: Path):
    parent_dir = temp_dir / "parent_dir"
    parent_dir.mkdir()
    file1 = parent_dir / "file1.txt"
    file1.touch()
    gitignore = parent_dir / ".gitignore"
    gitignore.touch()

    directory = Directory(dirPath=parent_dir)
    files = directory.list_all_files(ignoreFiles=[".gitignore"])

    assert file1 in files
    assert gitignore not in files

def test_Directory_model_config_frozen():
    with pytest.raises(ValueError):
        a = Directory(Path())
        a.dirPath= Path("toto")


def test_Directory_list_invalid_files(temp_dir: Path):
    test_dir = temp_dir / "test_directory"
    test_dir.mkdir()
    valid_file1 = test_dir / "valid_file1.txt"
    valid_file1.touch()
    invalid_file1 = test_dir / "invalid_file1.csv"
    invalid_file1.touch()
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    valid_file2 = sub_dir / "valid_file2.txt"
    valid_file2.touch()
    invalid_file2 = sub_dir / "invalid_file2.csv"
    invalid_file2.touch()
    
    valid_extension = ".txt"
    directory = Directory(test_dir)
    invalid_files = directory.list_invalid_files(validExtension=valid_extension)
    
    assert len(invalid_files) == 2
    assert valid_file1 not in invalid_files
    assert valid_file2 not in invalid_files
    assert invalid_file1 in invalid_files
    assert invalid_file2 in invalid_files


def test_Directory_list_valid_files(temp_dir: Path):
    test_dir = temp_dir / "test_directory"
    test_dir.mkdir()
    valid_file1 = test_dir / "valid_file1.txt"
    valid_file1.touch()
    invalid_file1 = test_dir / "invalid_file1.csv"
    invalid_file1.touch()
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    valid_file2 = sub_dir / "valid_file2.txt"
    valid_file2.touch()
    invalid_file2 = sub_dir / "invalid_file2.csv"
    invalid_file2.touch()
    
    valid_extension = ".txt"
    directory = Directory(test_dir)
    valid_files = directory.list_valid_files(validExtension=valid_extension)
    
    assert len(valid_files) == 2
    assert valid_file1 in valid_files
    assert valid_file2 in valid_files
    assert invalid_file1 not in valid_files
    assert invalid_file2 not in valid_files
