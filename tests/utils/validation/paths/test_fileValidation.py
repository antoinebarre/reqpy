""" UNIT TEST FOR FiLE VALIDATIO TOOLS OF UTILS
"""

# MODULE IMPORT
import reqpy
import pytest
import tempfile
import os

def test_validatefile():
    
    #create temp file
    temp = tempfile.NamedTemporaryFile()
    assert reqpy.utils.validation.validateFile(temp.name) == temp.name , "the file paht exist and shall be equal"
    temp.close() # the file is destroyed
    
    # no file
    with pytest.raises(ValueError) :
        _ = reqpy.utils.validation.validateFile(temp.name)
    
    
def test_validateFileExtension():
    """ test the tools to validate extension with a path"""
    
    from reqpy.utils.validation.__paths import InvalidFileExtension
    
    # bad extension
    with pytest.raises(InvalidFileExtension):
        reqpy.utils.validation.validateFileExtension("toto.c",".py")
    
    with pytest.raises(InvalidFileExtension):
        reqpy.utils.validation.validateFileExtension("toto.c",(".py",'.f'))
        
    # good extension
    path = reqpy.utils.validation.validateFileExtension("toto.py",(".py",'.f'))
    
    assert path == 'toto.py'
    

def test_isvalidExtension():
    """ test the tools to asses is a file has the appropriate extension"""
    assert reqpy.utils.validation.isValidExtension("toto.c",(".py",'.f')) == False
    assert reqpy.utils.validation.isValidExtension("toto.f",(".py",'.f')) == True
    
def test_validateExtensionDefinition():
    """ test the validation of the extension inputs"""
    
    
    
    # bad extension
    with pytest.raises(ValueError):
        reqpy.utils.validation.validateExtensionDefinition("toto")
        
    with pytest.raises(ValueError):
        reqpy.utils.validation.validateExtensionDefinition((".c","f"))
    
    # good extension definition
    
    val_init = (".c",".f")
    val = reqpy.utils.validation.validateExtensionDefinition(val_init)
    assert val is val_init
    
def test_validateFolder():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert reqpy.utils.validation.validateFolder(tmpdirname)==tmpdirname
        tmpName = tmpdirname
        
    with pytest.raises(ValueError):
        reqpy.utils.validation.validateFolder(tmpName)
        
  