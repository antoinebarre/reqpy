import pytest
from reqpy.requirement import RequirementsSet
from pathlib import Path

def test_create_fake_requirementset(tmp_path:Path):
    myFolder = tmp_path / "myFolder"

    myFolder.mkdir()

    [listFolder,listFile] = RequirementsSet(RequirementPath=myFolder).createFakeRequirementsSet()

    assert(all(folder.is_dir() for folder in listFolder))
    assert(all(folder.is_file() for folder in listFile))


