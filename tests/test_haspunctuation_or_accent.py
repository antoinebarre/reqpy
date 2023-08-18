import string
from reqpy.tools.strings import has_punctuation_or_accent

def test_has_punctuation_or_accent_no_punctuation_or_accent():
    text = "This is a simple text with no special characters"
    assert has_punctuation_or_accent(text) is False

def test_has_punctuation_or_accent_punctuation():
    text = "Hello, world!"
    assert has_punctuation_or_accent(text) is True

def test_has_punctuation_or_accent_accent():
    text = "Café"
    assert has_punctuation_or_accent(text) is True

def test_has_punctuation_or_accent_punctuation_and_accent():
    text = "Hello, Café!"
    assert has_punctuation_or_accent(text) is True

def test_has_punctuation_or_accent_unicode_characters():
    text = "Unicode characters: \u00A9"
    assert has_punctuation_or_accent(text) is True

def test_has_punctuation_or_accent_empty_string():
    text = ""
    assert has_punctuation_or_accent(text) is False

def test_has_punctuation_or_accent_only_punctuation():
    text = string.punctuation
    assert has_punctuation_or_accent(text) is True

def test_has_punctuation_or_accent_only_accent():
    text = "éèâêîôû"
    assert has_punctuation_or_accent(text) is True
