import pytest
from reqpy.tools.status import CheckStatus, CheckStatusList  # Import the CheckStatus class from your module

def test_valid_true_with_message():
    with pytest.raises(ValueError):
        CheckStatus(checkName="Test Check", valid=True, message="Some message")

def test_valid_true_without_message():
    status = CheckStatus(checkName="Test Check", valid=True, message="")
    assert status.checkName == "Test Check"
    assert status.valid == True
    assert status.message == ""

def test_createValid():
    status = CheckStatus.createValid(checkName="Test Check")
    assert status.checkName == "Test Check"
    assert status.valid == True
    assert status.message == ""

def test_valid_false_with_message():
    status = CheckStatus(checkName="Test Check", valid=False, message="Error message")
    assert status.checkName == "Test Check"
    assert status.valid == False
    assert status.message == "Error message"

def test_valid_false_without_message():
    with pytest.raises(TypeError):
        CheckStatus(checkName="Test Check", valid=False)

def test_str_valid_true():
    status = CheckStatus(checkName="Test Check", valid=True, message="")
    expected_output = "Check   : Test Check\nValid: True\n"
    assert str(status) == expected_output

def test_str_valid_false_with_message():
    status = CheckStatus(checkName="Test Check", valid=False, message="Error message")
    expected_output = "Check   : Test Check\nValid   : False\nMessages: Error message"
    assert str(status) == expected_output

def test_str_valid_false_without_message():
    status = CheckStatus(checkName="Test Check", valid=False, message="error")
    expected_output = "Check   : Test Check\nValid   : False\nMessages: error"
    assert str(status) == expected_output

def test_bad_checkName():
    with pytest.raises(ValueError):
        CheckStatus(checkName="",valid=True,message="")

def test_bad_message_with_failled_check():
    with pytest.raises(ValueError):
        CheckStatus(checkName="toto",valid=False,message="")



def test_checkstatus_list_constructor():
    checkstatus1 = CheckStatus(checkName="Check 1", valid=True, message="")
    checkstatus2 = CheckStatus(checkName="Check 2", valid=False, message="Error message")
    checkstatus3 = CheckStatus(checkName="Check 3", valid=True, message="")

    # Valid list of CheckStatus objects
    checkstatus_list = CheckStatusList([checkstatus1, checkstatus2, checkstatus3])
    assert len(checkstatus_list) == 3

    # Invalid list with non-CheckStatus items
    with pytest.raises(TypeError):
        CheckStatusList([checkstatus1, "not a CheckStatus", checkstatus3])

def test_checkstatus_list_append():
    checkstatus_list = CheckStatusList([])

    checkstatus = CheckStatus(checkName="Check 1", valid=True, message="")
    checkstatus_list.append(checkstatus)
    assert len(checkstatus_list) == 1

    with pytest.raises(TypeError):
        checkstatus_list.append("not a CheckStatus")

def test_checkstatus_list_extend():
    checkstatus_list1 = CheckStatusList([
        CheckStatus(checkName="Check 1", valid=True, message=""),
        CheckStatus(checkName="Check 2", valid=True, message="")
    ])

    checkstatus_list2 = CheckStatusList([
        CheckStatus(checkName="Check 3", valid=False, message="Error message"),
        CheckStatus(checkName="Check 4", valid=True, message="")
    ])

    checkstatus_list1.extend(checkstatus_list2)
    assert len(checkstatus_list1) == 4

    with pytest.raises(TypeError):
        checkstatus_list1.extend(["not a CheckStatus", "also not a CheckStatus"])

def test_checkstatus_list_is_valid():
    valid_checkstatus = CheckStatus(checkName="Check 1", valid=True, message="")
    invalid_checkstatus = CheckStatus(checkName="Check 2", valid=False, message="Error message")

    valid_list = CheckStatusList([valid_checkstatus, valid_checkstatus])
    invalid_list = CheckStatusList([valid_checkstatus, invalid_checkstatus])

    assert valid_list.is_valid() == True
    assert invalid_list.is_valid() == False


class TestCheckStatusList:

    @staticmethod
    def test_tostr_empty_list():
        check_list = CheckStatusList([])
        result = check_list.tostr()
        expected = (
            "+-------+----------+-----------+\n"
            "| Check | Is Valid | Rationale |\n"
            "+-------+----------+-----------+\n"
            "+-------+----------+-----------+"
        )


        assert result == expected

    @staticmethod
    def test_tostr_non_empty_list():
        check1 = CheckStatus(checkName="Check 1", valid=True, message="")
        check2 = CheckStatus(checkName="Check 2", valid=False, message="Invalid")
        check_list = CheckStatusList([check1, check2])
        result = check_list.tostr()
        expected = (
            "+---------+----------+-----------+\n"
            "| Check   | Is Valid | Rationale |\n"
            "+---------+----------+-----------+\n"
            "| Check 1 |   True   |           |\n"
            "| Check 2 |  False   | Invalid   |\n"
            "+---------+----------+-----------+"
        )
        assert result == expected

    @staticmethod
    def test_tostr_invalid_type():
        with pytest.raises(TypeError):
            invalid_check_list = CheckStatusList(["Not a CheckStatus object"])
            invalid_check_list.tostr()


