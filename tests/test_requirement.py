import pytest
from pathlib import Path
from reqpy import Requirement, ValidationStatus
from reqpy.exception import RequirementException,ReqpyIOException
from reqpy.constants import DEFAULT_REQPY_FILE_EXTENSION

@pytest.fixture
def valid_requirement_data():
    return {
        "title": "Valid Title",
        "description": "Description",
        "rationale": "Rationale",
        "validation_status": ValidationStatus.UNVALID,
    }

@pytest.fixture
def invalid_requirement_data():
    return {
        "title": "Invalid Title!?",
        "description": "Description",
        "rationale": "Rationale",
        "validation_status": ValidationStatus.UNVALID,
    }

def test_requirement_str(valid_requirement_data):
    expected_output = (
        ">>> Requirement Contents\n"
        "- title : Valid Title\n"
        "- description : Description\n"
        "- rationale : Rationale\n"
        "- validation_status : unvalid"
        )
    req = Requirement(**valid_requirement_data)
    
    assert str(req) == expected_output

def test_valid_requirement_init(valid_requirement_data):
    req = Requirement(**valid_requirement_data)
    assert req.title == "Valid Title"
    assert req.description == "Description"
    assert req.rationale == "Rationale"
    assert req.validation_status == ValidationStatus.UNVALID

def test_invalid_requirement_init(invalid_requirement_data):
    with pytest.raises(ValueError):
        Requirement(**invalid_requirement_data)

def test_title_must_start_with_alpha():
    with pytest.raises(ValueError):
        Requirement.title_must_start_with_alpha("123 Invalid Title")

    with pytest.raises(ValueError):
        Requirement.title_must_start_with_alpha("invalid Title")

def test_title_must_contain_only_characters_or_figures():
    with pytest.raises(ValueError):
        Requirement.title_must_contain_only_characters_or_figures("Invalid Title!?")

def test_read_valid_requirement(tmp_path, valid_requirement_data):
    file_path = tmp_path / "valid_requirement.yml"
    file_path.write_text("title: Valid Title\n")
    req = Requirement.read(filePath=file_path)
    assert req.title == "Valid Title"

def test_read_invalid_requirement(tmp_path, invalid_requirement_data):
    file_path = tmp_path / "invalid_requirement.yml"
    file_path.write_text("title: Invalid Title!?\n")
    with pytest.raises(ReqpyIOException):
        Requirement.read(filePath=file_path)

def test_get_file_Errors_valid_requirement(tmp_path, valid_requirement_data):
    file_path = tmp_path / "valid_requirement.yml"
    file_path.write_text("title: Valid Title\n")
    errors = Requirement.get_file_Errors(filePath=file_path)
    assert errors == ""

def test_get_file_Errors_invalid_requirement(tmp_path, invalid_requirement_data):
    file_path = tmp_path / "invalid_requirement.yml"
    file_path.write_text("title: Invalid Title!?\n")
    errors = Requirement.get_file_Errors(filePath=file_path)
    assert "Impossible to parse the YAML file" in errors

def test_is_ValidRequirementFile(tmp_path, valid_requirement_data):
    file_path = tmp_path / ("valid_requirement" + DEFAULT_REQPY_FILE_EXTENSION)
    file_path.write_text("title: Valid Title\n")
    assert Requirement.is_ValidRequirementFile(filePath=file_path) is True

def test_is_InvalidRequirementFile(tmp_path, invalid_requirement_data):
    file_path = tmp_path / "invalid_requirement.yml"
    file_path.write_text("title: Invalid Title!?\n")
    assert Requirement.is_ValidRequirementFile(filePath=file_path) is False

    file_path = tmp_path / "invalid_requirement.yaml"
    file_path.write_text("title: Invalid Title\n")
    assert Requirement.is_ValidRequirementFile(filePath=file_path) is False