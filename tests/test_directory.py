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
