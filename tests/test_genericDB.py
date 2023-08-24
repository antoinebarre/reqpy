import pytest
from unittest.mock import Mock
from reqpy.__DB import GenericDB
from reqpy.tools.status import CheckStatus, CheckStatusList
from reqpy.exception import ReqpyDBException
from pathlib import Path
from unittest.mock import Mock, patch

class TestGenericDB:

    @staticmethod
    def test_folder_path_validation_valid():
        db = GenericDB(folderPath=Path(), allowSubfolders=True, allowAdditionalFiles=True)
        assert db.folderPath == Path()

    @staticmethod
    def test_folder_path_validation_invalid():
        with pytest.raises(ValueError):
            db = GenericDB(folderPath=Path("nonexistent_folder"), allowSubfolders=True, allowAdditionalFiles=True)

    @staticmethod
    def test_copy_folders_files_valid(capsys, tmp_path: Path):
        myFolder = tmp_path / "test_data"
        myFolder.mkdir()
        myFolder2 = myFolder / "test"
        myFolder2.mkdir()
        myFile = myFolder / "file1.txt"
        myFile.touch()
        myFile2 = myFolder2 / "file2.txt"
        myFile2.touch()
        
        db = GenericDB(folderPath=myFolder, allowSubfolders=True, allowAdditionalFiles=True)
        destination_dir = tmp_path / "copy_test"
        db.copyFoldersFiles(destinationDir=destination_dir, show_console=True)

        assert (destination_dir / "file1.txt").is_file()
        assert (destination_dir/ 'test' / "file2.txt").is_file()
        
    # @staticmethod
    # def test_copy_folders_files_invalid(capsys, tmp_path):
    #     db = GenericDB(folderPath=Path("nonexistent_folder"), allowSubfolders=True, allowAdditionalFiles=True)
    #     destination_dir = tmp_path / "copy_test"
    #     with pytest.raises(Exception):
    #         db.copyFoldersFiles(destinationDir=destination_dir, show_console=True)
        
    # @staticmethod
    # def test_validate_database_valid():
    #     db = GenericDB(folderPath=Path("test_data"), allowSubfolders=True, allowAdditionalFiles=True)
    #     result = db.validateDataBase()
    #     assert result.is_valid() is True

    @staticmethod
    def test_copy_folders_files_additional_files_copy_error(tmp_path:Path):
        myFolder = tmp_path / "test_data"
        myFolder.mkdir()
        (myFolder / "file.txt").touch()
        db = GenericDB(folderPath=myFolder, allowSubfolders=True, allowAdditionalFiles=True)
        destination_dir = tmp_path / "copy_test"

        with patch("reqpy.__DB.copy",side_effect=Exception('COPY ERROR')):
            with pytest.raises(ReqpyDBException):
                db.copyFoldersFiles(destinationDir=destination_dir, show_console=True)

    @staticmethod
    def test_validate_subfolder_with_allowed_subfolders():
        db = GenericDB(folderPath=Path(), allowSubfolders=True, allowAdditionalFiles=False)
        result = db._GenericDB__validateSubFolder()
        assert result.valid is True

    @staticmethod
    def test_validate_subfolder_with_disallowed_subfolders():
        db = GenericDB(folderPath=Path(), allowSubfolders=False, allowAdditionalFiles=False)
        result = db._GenericDB__validateSubFolder()
        assert result.valid is False

    @staticmethod
    def test_validate_subfolder_with_empty_folder(tmp_path:Path):
        empty_folder = tmp_path / "test"
        empty_folder.mkdir()
        db = GenericDB(folderPath=empty_folder, allowSubfolders=False, allowAdditionalFiles=False)
        result = db._GenericDB__validateSubFolder()
        assert result.valid is True

    @staticmethod
    def test_validate_subfolder_with_allowed_subfolders_and_empty_folder(tmp_path:Path):
        empty_folder = tmp_path / "test"
        empty_folder.mkdir()
        db = GenericDB(folderPath=empty_folder, allowSubfolders=True, allowAdditionalFiles=False)
        result = db._GenericDB__validateSubFolder()
        assert result.valid is True

    @staticmethod
    def test_validate_subfolder_with_existing_files_and_allowed_subfolders(tmp_path:Path):
        folder_with_files = tmp_path / "test"
        folder_with_files.mkdir()
        (folder_with_files / "file1.txt").touch()
        (folder_with_files / "file2.txt").touch()
        db = GenericDB(folderPath=folder_with_files, allowSubfolders=True, allowAdditionalFiles=False)
        result = db._GenericDB__validateSubFolder()
        assert result.valid is True
   
    @staticmethod
    def test_validate_additional_files_with_allowed_files(tmp_path):
        db = GenericDB(folderPath=tmp_path, allowSubfolders=False, allowAdditionalFiles=True)
        result = db._GenericDB__validateAdditionalFiles()
        assert result.valid is True

    @staticmethod
    def test_validate_additional_files_with_disallowed_files(tmp_path:Path):
        (tmp_path / "file.txt").touch()
        db = GenericDB(folderPath=tmp_path, allowSubfolders=False, allowAdditionalFiles=False)
        result = db._GenericDB__validateAdditionalFiles()
        assert result.valid is False

    @staticmethod
    def test_validate_additional_files_with_empty_folder(tmp_path):
        empty_folder = tmp_path / "empty_folder"
        empty_folder.mkdir()
        db = GenericDB(folderPath=empty_folder, allowSubfolders=False, allowAdditionalFiles=True)
        result = db._GenericDB__validateAdditionalFiles()
        assert result.valid is True

    @staticmethod
    def test_validate_additional_files_with_valid_files(tmp_path):
        folder_with_files = tmp_path / "folder_with_files"
        folder_with_files.mkdir()
        (folder_with_files / "file1.txt").touch()
        (folder_with_files / "file2.txt").touch()
        db = GenericDB(folderPath=folder_with_files, allowSubfolders=False, allowAdditionalFiles=True)
        result = db._GenericDB__validateAdditionalFiles()
        assert result.valid is True

    @staticmethod
    def test_validate_additional_files_with_invalid_files(tmp_path):
        folder_with_files = tmp_path / "folder_with_files"
        folder_with_files.mkdir()
        (folder_with_files / "file1.invalid").touch()
        (folder_with_files / "file2.invalid").touch()
        db = GenericDB(folderPath=folder_with_files, allowSubfolders=False, allowAdditionalFiles=False)
        result = db._GenericDB__validateAdditionalFiles()
        assert result.valid is False
    
    # @staticmethod
    # @patch("shutil.copy")
    # @patch("builtins.print")
    # def test_copy_folders_structure_valid(mock_print, mock_copy, tmp_path):
    #     myPath = tmp_path / "db"
    #     myPath.mkdir()
    #     db = GenericDB(folderPath=myPath, allowSubfolders=True, allowAdditionalFiles=False)
    #     destination_dir = tmp_path / "copy_test"
    #     db._GenericDB__copy_folders_structure(destinationDir=destination_dir, show_console=True)

    #     mock_copy.assert_not_called()
    #     mock_print.assert_called_once_with("Copy of the folder structure to", destination_dir)
    
    @staticmethod
    def test_copy_folders_files_additional_files_mkdir_error(tmp_path:Path):
        myFolder = tmp_path / "test_data"
        myFolder.mkdir()
        (myFolder / "dfgdfg").mkdir()
        db = GenericDB(folderPath=myFolder, allowSubfolders=True, allowAdditionalFiles=True)
        destination_dir = tmp_path / "copy_test"

        with patch("reqpy.__DB.Path.mkdir",side_effect=Exception('MKDIR ERROR')):
            with pytest.raises(ReqpyDBException):
                db._GenericDB__copy_folders_structure(destinationDir=destination_dir, show_console=True)
    @staticmethod
    def test_copy_folders_files_invalideDB(tmp_path:Path):
        mydir = tmp_path / "tttt"
        mydir.mkdir()
        (mydir / "file.txt").touch()
        destination = tmp_path / "final"
        destination.mkdir()

        db = GenericDB(folderPath=mydir, allowSubfolders=True, allowAdditionalFiles=False)

        with pytest.raises(ReqpyDBException):
            db.copyFoldersFiles(destinationDir=destination,show_console=False)