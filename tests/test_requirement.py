import pytest
from datetime import datetime
from pathlib import Path
from reqpy import Requirement,ReqFile
from reqpy.__settings import RequirementSettings, RequirementFileSettings

# Test the Requirement class
class TestRequirement:
    """ Test Requirement class"""
    def test_default_values(self):
        """
        Test that a Requirement instance is initialized with default values.
        """
        requirement = Requirement()
        assert requirement.title == "Requirement Title"
        assert requirement.detail == "Description of the requirement as Markdown"
        assert requirement.validation_status == "UNVALID"
        assert isinstance(requirement.creation_date, datetime)

    def test_title_min_length(self):
        """
        Test that a ValueError is raised when the title is below the minimum length.
        """
        with pytest.raises(ValueError):
            Requirement(title="Ab")

    def test_title_max_length(self):
        """
        Test that a ValueError is raised when the title exceeds the maximum length.
        """
        with pytest.raises(ValueError):
            Requirement(title="A" * (RequirementSettings.max_title_length + 1))

    def test_title_start_with_alpha(self):
        """
        Test that a ValueError is raised when the title does not start with an alphabet character.
        """
        with pytest.raises(ValueError):
            Requirement(title="123 Requirement")

    def test_title_characters_or_figure(self):
        """
        Test that a ValueError is raised when the title contains punctuation or accent characters.
        """
        with pytest.raises(ValueError):
            Requirement(title="Requirement!")

    # Add more test cases for other methods or properties in the Requirement class

# Test the ReqFile class
class TestReqFile:  
    @pytest.fixture
    def temp_file(self, tmp_path):
        """
        Fixture that creates a temporary file and returns its path.
        """
        file_path = tmp_path / "temp_file.yml"
        req_file = ReqFile(path=file_path)
        requirement = Requirement(title="Test Requirement", detail="This is a test requirement.")
        req_file.write(requirement)
        return str(file_path)

    def test_validate_extension_valid(self):
        """
        Test that the extension validation passes for a valid file path.
        """
        req_file = ReqFile(path="requirements.yml")
        validated_path = req_file.validate_extension(req_file.path)
        assert validated_path == Path("requirements.yml")

    def test_validate_extension_invalid(self):
        """
        Test that a ValueError is raised when the extension validation fails.
        """
        with pytest.raises(ValueError):
            req_file = ReqFile(path="requirements.docx")

    def test_exists(self,temp_file):
        """
        Test that the exists() method returns True when the file exists.
        """
        req_file = ReqFile(path=temp_file)
        assert req_file.exists() is True

    def test_exists_file_not_found(self):
        """
        Test that the exists() method returns False when the file does not exist.
        """
        req_file = ReqFile(path="nonexistent_file.yml")
        assert req_file.exists() == False

    def test_read_file_exists(self,temp_file):
        """
        Test that the read() method successfully 
        reads the requirement file and returns 
        a Requirement object.
        """
        req_file = ReqFile(path=temp_file)
        requirement = req_file.read()
        assert isinstance(requirement, Requirement)

    def test_read_file_not_found(self):
        """
        Test that a FileNotFoundError is raised when 
        the read() method is called on a non-existent file.
        """
        req_file = ReqFile(path="nonexistent_file.yml")
        with pytest.raises(FileNotFoundError):
            req_file.read()

    def test_write(self):
        """
        Test that the write() method successfully 
        writes a YAML file based on the Requirement object.
        """
        req_file = ReqFile(path="output.yml")
        requirement = Requirement(title="Test Requirement", detail="This is a test requirement.")
        req_file.write(requirement)
        assert req_file.exists() is True

    # Add more test cases for other methods in the ReqFile class

