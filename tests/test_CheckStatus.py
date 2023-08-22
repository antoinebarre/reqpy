import pytest
from reqpy.tools.status import CheckStatus, CheckStatusList  # Import the CheckStatus class from your module

def test_valid_true_with_message():
    with pytest.raises(ValueError):
        CheckStatus(check="Test Check", valid=True, message="Some message")

def test_valid_true_without_message():
    status = CheckStatus(check="Test Check", valid=True, message="")
    assert status.check == "Test Check"
    assert status.valid == True
    assert status.message == ""

def test_createValid():
    status = CheckStatus.createValid(checkName="Test Check")
    assert status.check == "Test Check"
    assert status.valid == True
    assert status.message == ""

def test_valid_false_with_message():
    status = CheckStatus(check="Test Check", valid=False, message="Error message")
    assert status.check == "Test Check"
    assert status.valid == False
    assert status.message == "Error message"

def test_valid_false_without_message():
    with pytest.raises(TypeError):
        CheckStatus(check="Test Check", valid=False)

def test_str_valid_true():
    status = CheckStatus(check="Test Check", valid=True, message="")
    expected_output = "Check   : Test Check\nValid: True\n"
    assert str(status) == expected_output

def test_str_valid_false_with_message():
    status = CheckStatus(check="Test Check", valid=False, message="Error message")
    expected_output = "Check   : Test Check\nValid   : False\nMessages: Error message"
    assert str(status) == expected_output

def test_str_valid_false_without_message():
    status = CheckStatus(check="Test Check", valid=False, message="error")
    expected_output = "Check   : Test Check\nValid   : False\nMessages: error"
    assert str(status) == expected_output

def test_bad_checkName():
    with pytest.raises(ValueError):
        CheckStatus(check="",valid=True,message="")

def test_bad_message_with_failled_check():
    with pytest.raises(ValueError):
        CheckStatus(check="toto",valid=False,message="")



def test_checkstatus_list_constructor():
    checkstatus1 = CheckStatus(check="Check 1", valid=True, message="")
    checkstatus2 = CheckStatus(check="Check 2", valid=False, message="Error message")
    checkstatus3 = CheckStatus(check="Check 3", valid=True, message="")

    # Valid list of CheckStatus objects
    checkstatus_list = CheckStatusList([checkstatus1, checkstatus2, checkstatus3])
    assert len(checkstatus_list) == 3

    # Invalid list with non-CheckStatus items
    with pytest.raises(TypeError):
        CheckStatusList([checkstatus1, "not a CheckStatus", checkstatus3])

def test_checkstatus_list_append():
    checkstatus_list = CheckStatusList([])

    checkstatus = CheckStatus(check="Check 1", valid=True, message="")
    checkstatus_list.append(checkstatus)
    assert len(checkstatus_list) == 1

    with pytest.raises(TypeError):
        checkstatus_list.append("not a CheckStatus")

def test_checkstatus_list_extend():
    checkstatus_list1 = CheckStatusList([
        CheckStatus(check="Check 1", valid=True, message=""),
        CheckStatus(check="Check 2", valid=True, message="")
    ])

    checkstatus_list2 = CheckStatusList([
        CheckStatus(check="Check 3", valid=False, message="Error message"),
        CheckStatus(check="Check 4", valid=True, message="")
    ])

    checkstatus_list1.extend(checkstatus_list2)
    assert len(checkstatus_list1) == 4

    with pytest.raises(TypeError):
        checkstatus_list1.extend(["not a CheckStatus", "also not a CheckStatus"])

def test_checkstatus_list_is_valid():
    valid_checkstatus = CheckStatus(check="Check 1", valid=True, message="")
    invalid_checkstatus = CheckStatus(check="Check 2", valid=False, message="Error message")

    valid_list = CheckStatusList([valid_checkstatus, valid_checkstatus])
    invalid_list = CheckStatusList([valid_checkstatus, invalid_checkstatus])

    assert valid_list.is_valid() == True
    assert invalid_list.is_valid() == False
