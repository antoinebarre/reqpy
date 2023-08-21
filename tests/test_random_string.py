import random
import string
from reqpy.tools.strings import generate_paragraph, generate_title
import pytest

# Test generate_paragraph function
def test_generate_paragraph():
    max_characters = 200
    paragraph = generate_paragraph(max_characters)
    assert isinstance(paragraph, str)
    assert len(paragraph) <= max_characters

def test_generate_paragraph_invalid_max_characters():
    with pytest.raises(ValueError):
        generate_paragraph(-100)

# Test generate_title function
def test_generate_title():
    min_characters = 10
    max_characters = 20
    title = generate_title(min_characters, max_characters)
    assert isinstance(title, str)
    assert min_characters <= len(title) <= max_characters
    assert title[0].isupper()
    assert any(char in string.punctuation for char in title) is False

def test_generate_title_invalid_min_characters():
    with pytest.raises(ValueError):
        generate_title(-10, 20)

def test_generate_title_invalid_max_characters():
    with pytest.raises(ValueError):
        generate_title(10, 5)

def test_generate_title_min_greater_than_max_characters():
    with pytest.raises(ValueError):
        generate_title(20, 10)
