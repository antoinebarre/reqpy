# ~~~~~~ UNIT TEST FOR ERROR MESSAGE ~~~~~~ #

# IMPORT PACKAGE
import reqpy


def test_errormsg():
    # check the execution of createErrorMessage : generate a string without error

    assert isinstance(reqpy.utils.exception.createErrorMessage(
        errorMsg="toto",
        expected="titi",
        current="tata" 
    ),str)