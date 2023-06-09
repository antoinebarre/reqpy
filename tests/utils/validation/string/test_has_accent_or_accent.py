import pytest
from reqpy.utils.validation import has_punctuation_or_accent

@pytest.mark.parametrize("text, expected_result", [
    ("Hello World!", True),  # Contains punctuation characters
    ("éàü", True),  # Contains accents
    ("NoPunctuationOrAccent", False),  # No punctuation characters or accents
    ("", False),  # Empty string
    ("12345", False),  # Only alphanumeric characters
    (" ", False),  # Only whitespace
    ("áéíóú", True),  # Contains accents
    (".,!?¿¡", True),  # Contains punctuation characters
    ("Acçènt", True),  # Contains an accent
])
def test_has_punctuation_or_accent(text, expected_result):
    assert has_punctuation_or_accent(text) == expected_result
