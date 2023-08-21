import pytest
from reqpy.tools.status import CheckStatus

def test_empty_checkstatus():
    status = CheckStatus(valid=True, message=[])
    assert status.valid == True
    assert status.message == []
    assert status.nb_status == 0

def test_valid_checkstatus_with_messages():
    status = CheckStatus(valid=True, message=["Message 1", "Message 2"])
    assert status.valid == True
    assert status.message == []
    assert status.nb_status == 0

def test_invalid_checkstatus():
    status = CheckStatus(valid=False, message=["Error message"])
    assert status.valid == False
    assert status.message == ["Error message"]
    assert status.nb_status == 1

def test_add_checkstatuses():
    status1 = CheckStatus(valid=True, message=["Message 1"])
    status2 = CheckStatus(valid=False, message=["Error message"])
    combined_status = status1 + status2
    assert combined_status.valid == False
    assert combined_status.message == ["Error message"]
    assert combined_status.nb_status == 1

def test_str_method():
    # Case 1: Valid status with no messages
    status1 = CheckStatus(valid=True, message=[])
    assert str(status1) == "Valid: True\n"

    # Case 2: Valid status with messages
    status2 = CheckStatus(valid=True, message=["Message 1", "Message 2"])
    expected_output2 = "Valid: True\n"
    assert str(status2) == expected_output2

    # Case 3: Invalid status with no messages
    status3 = CheckStatus(valid=False, message=[])
    expected_output3 = "Valid: False\n"
    assert str(status3) == expected_output3

    # Case 4: Invalid status with messages
    status4 = CheckStatus(valid=False, message=["Error 1", "Error 2"])
    expected_output4 = "Valid: False\nMessages: (nb of issues: 2)\nError 1\nError 2"
    assert str(status4) == expected_output4