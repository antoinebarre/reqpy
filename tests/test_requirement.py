import pytest
from pathlib import Path
from typing import Any
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

def test_requirement_str(valid_requirement_data: dict[str, Any]):
    expected_output = (
        ">>> Requirement Contents\n"
        "- title : Valid Title\n"
        "- description : Description\n"
        "- rationale : Rationale\n"
        "- validation_status : unvalid"
        )
    req = Requirement(**valid_requirement_data)
    
    assert str(req) == expected_output

def test_valid_requirement_init(valid_requirement_data: dict[str, Any]):
    req = Requirement(**valid_requirement_data)
    assert req.title == "Valid Title"
    assert req.description == "Description"
    assert req.rationale == "Rationale"
    assert req.validation_status == ValidationStatus.UNVALID

def test_invalid_requirement_init(invalid_requirement_data: dict[str, Any]):
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

def test_read_valid_requirement(tmp_path: Path, valid_requirement_data: dict[str, Any]):
    file_path = tmp_path / "valid_requirement.yml"
    file_path.write_text("title: Valid Title\n")
    req = Requirement.read(filePath=file_path)
    assert req.title == "Valid Title"

def test_read_invalid_requirement(tmp_path: Path, invalid_requirement_data: dict[str, Any]):
    file_path = tmp_path / "invalid_requirement.yml"
    file_path.write_text("title: Invalid Title!?\n")
    with pytest.raises(ReqpyIOException):
        Requirement.read(filePath=file_path)

def test_get_file_Errors_valid_requirement(tmp_path: Path, valid_requirement_data: dict[str, Any]):
    file_path = tmp_path / "valid_requirement.yml"
    file_path.write_text("title: Valid Title\n")
    errors = Requirement.get_file_Errors(filePath=file_path)
    assert errors == ""

def test_get_file_Errors_invalid_requirement(tmp_path: Path, invalid_requirement_data: dict[str, Any]):
    file_path = tmp_path / "invalid_requirement.yml"
    file_path.write_text("title: Invalid Title!?\n")
    errors = Requirement.get_file_Errors(filePath=file_path)
    assert "Impossible to parse the YAML file" in errors

def test_is_ValidRequirementFile(tmp_path: Path, valid_requirement_data: dict[str, Any]):
    file_path = tmp_path / ("valid_requirement" + DEFAULT_REQPY_FILE_EXTENSION)
    file_path.write_text("title: Valid Title\n")
    assert Requirement.is_ValidRequirementFile(filePath=file_path) is True

def test_is_InvalidRequirementFile(tmp_path: Path, invalid_requirement_data: dict[str, Any]):
    file_path = tmp_path / "invalid_requirement.yml"
    file_path.write_text("title: Invalid Title!?\n")
    assert Requirement.is_ValidRequirementFile(filePath=file_path) is False

    file_path = tmp_path / "invalid_requirement.yaml"
    file_path.write_text("title: Invalid Title\n")
    assert Requirement.is_ValidRequirementFile(filePath=file_path) is False


@pytest.fixture
def mock_generate_title(mocker):
    return mocker.patch('reqpy.requirement.generate_title')

@pytest.fixture
def mock_generate_paragraph(mocker):
    return mocker.patch('reqpy.requirement.generate_paragraph')

def test_create_fake_requirement(mock_generate_title: Any, mock_generate_paragraph: Any):
    mock_generate_title.return_value = "Mock Title"
    mock_generate_paragraph.return_value = "Mock Description"

    fake_requirement = Requirement.createFakeRequirement()

    assert fake_requirement.title == "Mock Title"
    assert fake_requirement.description == "Mock Description"
    assert fake_requirement.rationale == "Mock Description"

def test_write_fake_requirement_file(tmp_path: Path):
    file_path = Requirement.writeFakeRequirementFile(tmp_path)
    assert file_path.exists()
    assert file_path.is_file()

    # Check if the written file is a valid requirement file
    assert Requirement.is_ValidRequirementFile(file_path)

    # Read the written requirement and verify its attributes
    req = Requirement.read(file_path)
    assert req.title
    assert req.description
    assert req.rationale

def test_write_fake_requirement_file_multiple_times(tmp_path: Path):
    num_files = 5
    file_paths = []

    for _ in range(num_files):
        file_path = Requirement.writeFakeRequirementFile(tmp_path)
        file_paths.append(file_path)

    # Check if all written files are valid requirement files
    for file_path in file_paths:
        assert file_path.exists()
        assert file_path.is_file()
        assert Requirement.is_ValidRequirementFile(file_path)

def test_validate_requirement_file():
    # Valid Requirement
    valid_requirement = Requirement(
        title="Valid Requirement",
        description="This is a valid requirement.",
        rationale="Valid requirement rationale."
    )
    valid_file_path = Path("valid_requirement.yml")
    valid_requirement.write(filePath=valid_file_path)
    
    # Invalid Requirement
    invalid_file_path = Path("invalid_requirement.yml")
    with open(invalid_file_path, "w") as f:
        f.write("This is not a valid YAML content.")
    
    # Test valid requirement file
    valid_status = Requirement.validateRequirementFile(filePath=valid_file_path)
    assert valid_status.valid == True
    assert valid_status.message == []
    
    # Test invalid requirement file
    invalid_status = Requirement.validateRequirementFile(filePath=invalid_file_path)
    assert invalid_status.valid == False
    assert len(invalid_status.message) > 0

    # Clean up
    valid_file_path.unlink()
    invalid_file_path.unlink()


