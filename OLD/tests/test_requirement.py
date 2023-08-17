import pytest
from datetime import datetime
from pathlib import Path
from reqpy.requirements import Requirement, RequirementFileError, RequiqrementFolderError

@pytest.fixture
def requirement_data():
    return {
        "title": "Test Requirement",
        "detail": "Test requirement description",
        "validation_status": "UNVALID",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }

def test_requirement_creation(requirement_data):
    """
    Test case for creating a Requirement object
    """
    requirement = Requirement(**requirement_data)
    assert requirement.title == requirement_data["title"]
    assert requirement.detail == requirement_data["detail"]
    assert requirement.validation_status == requirement_data["validation_status"]
    assert isinstance(requirement.creation_date, datetime)
    assert requirement.rationale == requirement_data["rationale"]

def test_requirement_validation_status_validation():
    """
    Test case for validating the validation_status attribute.
    """
    requirement_data = {
        "title": "Test Requirement",
        "detail": "Test requirement description",
        "validation_status": "TOTO",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }
    with pytest.raises(ValueError):
        Requirement(**requirement_data)

def test_requirement_title_validation():
    """
    Test case for validating the title attribute.
    """
    requirement_data = {
        "title": "123 Title",
        "detail": "Test requirement description",
        "validation_status": "UNVALID",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }
    with pytest.raises(ValueError):
        Requirement(**requirement_data)

    requirement_data = {
        "title": "abc Title",
        "detail": "Test requirement description",
        "validation_status": "UNVALID",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }
    with pytest.raises(ValueError):
        Requirement(**requirement_data)
    

def test_requirement_file_handling(tmpdir):
    """
    Test case for file handling methods of Requirement class.
    """
    requirement_data = {
        "title": "Test Requirement",
        "detail": "Test requirement description",
        "validation_status": "UNVALID",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }
    requirement = Requirement(**requirement_data)
    folder_path = Path(tmpdir)
    
    # Test write() method
    path2test = requirement.write(folderPath=folder_path)
    file_path = folder_path / requirement.get_valid_fileName()
    assert file_path.exists()
    assert file_path == path2test
    
    # Test read() method
    read_requirement = Requirement.read(filePath=file_path)
    assert read_requirement.title == requirement.title
    assert read_requirement.detail == requirement.detail
    assert read_requirement.validation_status == requirement.validation_status
    assert read_requirement.creation_date == requirement.creation_date
    assert read_requirement.rationale == requirement.rationale
    
    # Test rename() method
    old_name = folder_path / "tototata.yml"
    file_path.rename(old_name)
    new_file_path = requirement.rename(old_name)
    assert new_file_path != old_name
    assert new_file_path.exists()
    
    # Test is_valid_fileName() method
    print(new_file_path,requirement.title)
    assert requirement.is_valid_fileName(new_file_path)
    invalid_file_path = folder_path / "invalid_file.txt"
    assert not requirement.is_valid_fileName(invalid_file_path)
    
    # Test get_file_Errors() method
    errors = Requirement.get_file_Errors(invalid_file_path)
    assert len(errors) > 0

def test_requirement_file_handling_exceptions(tmpdir):
    """
    Test case for file handling exceptions of Requirement class.
    """
    requirement_data = {
        "title": "Test Requirement",
        "detail": "Test requirement description",
        "validation_status": "UNVALID",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }
    requirement = Requirement(**requirement_data)
    folder_path = Path(tmpdir)
    
    # Test write() method with invalid folder path
    invalid_folder_path = folder_path / "invalid_folder"
    with pytest.raises(RequiqrementFolderError):
        requirement.write(folderPath=invalid_folder_path)
    
    # Test read() method with invalid file path
    invalid_file_path = folder_path / "invalid_file.txt"
    with pytest.raises(RequirementFileError):
        Requirement.read(filePath=invalid_file_path)
    
    # Test rename() method with invalid file path
    invalid_file_path = folder_path / "invalid_file.txt"
    with pytest.raises(RequirementFileError):
        requirement.rename(invalid_file_path)

def test_requirement_validation_tools(tmpdir):
    """
    Test case for validation tools of Requirement class.
    """
    requirement_data = {
        "title": "Test Requirement",
        "detail": "Test requirement description",
        "validation_status": "UNVALID",
        "creation_date": datetime.now(),
        "rationale": "Test requirement rationale"
    }
    requirement = Requirement(**requirement_data)
    folder_path = Path(tmpdir)

    reqFile =requirement.write(folderPath=folder_path)

    # Test is_RequirementFile() method
    assert Requirement.is_RequirementFile(reqFile)
    invalid_file_path = reqFile.rename(folder_path / "invalid_file.txt")
    assert not Requirement.is_RequirementFile(invalid_file_path)
    
    # Test is_valid_RequirementFile_Name() method
    invalid_file_path = invalid_file_path.rename(folder_path / "invalid_requirement.yml")
    assert not Requirement.is_valid_RequirementFile_Name(invalid_file_path)

    valid_file_path = invalid_file_path.rename(reqFile)
    assert Requirement.is_valid_RequirementFile_Name(valid_file_path)
