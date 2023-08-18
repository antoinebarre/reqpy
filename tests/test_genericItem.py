import pytest
from pathlib import Path
from io import StringIO
from unittest.mock import patch
from enum import StrEnum, auto
from pydantic import BaseModel
from reqpy.__genericItem import GenericItem
from reqpy.constants import DEFAULT_REQPY_FILE_EXTENSION
from reqpy.exception import ReqpyIOException,ReqpyPathException
# create a fake class pydantic class

class DummyEnum(StrEnum):
    UNVALID = auto()
    VALID = auto()
    def __str__(self):
        return "DUMMY"

class DummyClass(BaseModel, GenericItem):
    A: str
    B: float
    C: bool
    D: DummyEnum

    def __str__(self):
        return GenericItem.__str__(self)
    

@pytest.fixture()
def generic_item_instance():
    return DummyClass(A="test\ntoto",B=1.3,C=False,D=DummyEnum.UNVALID)


class Test_GenericClass():
    def test_generic_item_str(self,generic_item_instance):
        expected_output = (
            ">>> DummyClass Contents\n"
            "- A : test\ntoto\n"
            "- B : 1.3\n"
            "- C : False\n"
            "- D : DUMMY"
        )
        assert str(generic_item_instance) == expected_output

        #assert captured.out.strip() == expected_output

    def test_generic_item_attributesList(self, generic_item_instance):
        attributes_list = generic_item_instance.attributesList
        assert "_defaultExtension" not in attributes_list
        assert "A" in attributes_list
        assert "B" in attributes_list
        assert "C" in attributes_list
        assert "D" in attributes_list
        assert len(attributes_list) == 4

    def test_generic_item_className(self,generic_item_instance):
        assert generic_item_instance.className == "DummyClass"

    def test_generic_item_toDict(self,generic_item_instance):
        data = generic_item_instance.toDict()
        assert "_defaultExtension" not in data
        assert data["A"] == "test\ntoto"
        assert data["B"] == 1.3
        assert data["C"] == False
        assert data["D"] == "DUMMY"


    def test_generic_item_write(self,tmp_path, generic_item_instance):
        file_path: Path = tmp_path / ("generic_item" + DEFAULT_REQPY_FILE_EXTENSION)
        generic_item_instance.write(filePath=file_path)
        assert file_path.is_file()
        txt = file_path.read_text()
        print(txt)

        expected_output=(
            "A: |-\n"
            "  test\n"
            "  toto\n"
            "B: 1.3\n"
            "C: false\n"
            "D: DUMMY\n"
        )
        print(expected_output)
        
        assert txt == expected_output

    def test_generic_item_read2dict(self,tmp_path, generic_item_instance):
        file_path: Path = tmp_path / ("generic_item."+DEFAULT_REQPY_FILE_EXTENSION)
        data = {"_defaultExtension": ".reqpy"}

        data=(
            "A: |-\n"
            "  test\n"
            "  toto\n"
            "B: 1.3\n"
            "C: false\n"
            "D: VALID\n"
        )

        expectedResult ={
            "A": "test\ntoto",
            "B": 1.3,
            "C": False,
            "D": "VALID",
        }
        # write file
        file_path.write_text(data)

        read_data = GenericItem.read2dict(file_path)
        assert read_data['A'] == expectedResult['A']
        assert read_data['B'] == expectedResult['B']
        assert read_data['C'] == expectedResult['C']
        assert read_data['D'] == expectedResult['D']

def test_generic_item_read2dict_invalid_yaml(tmp_path, generic_item_instance):
    file_path = tmp_path / ("generic_item."+DEFAULT_REQPY_FILE_EXTENSION)
    with open(file_path, "w") as file:
        file.write("invalid: : yaml")

    with pytest.raises(ReqpyIOException):
        GenericItem.read2dict(file_path)

def test_generic_item_write_exception(tmp_path, generic_item_instance):
    with patch("reqpy.tools.paths.validateCorrectFileExtension", side_effect=Exception):
        with pytest.raises(Exception):
            generic_item_instance.write(tmp_path / ("test"+"txt"))

def test_generic_item_read2dict_exception(generic_item_instance):
    with patch("reqpy.tools.paths.validateFileExistence", side_effect=Exception):
        with pytest.raises(ReqpyPathException):
            GenericItem.read2dict(Path("invalid.txt"))
