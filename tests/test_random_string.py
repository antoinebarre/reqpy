import random
import string
from reqpy.tools.strings import generate_paragraph, generate_title, random_string, random_Title
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

def test_random_string_default_length():
    result = random_string()
    assert isinstance(result, str)
    assert 8 <= len(result) <= 14
    assert all(c in string.ascii_lowercase + string.digits + " " for c in result)

def test_random_string_custom_length():
    result = random_string(min_length=8, max_length=15)
    assert isinstance(result, str)
    assert 8 <= len(result) <= 15
    assert all(c in string.ascii_lowercase + string.digits + " " for c in result)

def test_random_string_empty_string():
    assert ""==random_string(min_length=0, max_length=0)

def test_random_string_invalid_length():
    with pytest.raises(ValueError):
        random_string(min_length=15, max_length=10)

def test_random_string_randomness():
    random_strings = [random_string() for _ in range(100)]
    assert len(set(random_strings)) > 1  # Check that multiple random strings are generated


def test_random_string_default_length():
    result = random_string()
    assert isinstance(result, str)
    assert 8 <= len(result) <= 14
    assert all(c in string.ascii_lowercase + string.digits + " " for c in result)

def test_random_string_custom_length():
    result = random_string(min_length=10, max_length=20)
    assert isinstance(result, str)
    assert 10 <= len(result) <= 20
    assert all(c in string.ascii_lowercase + string.digits + " " for c in result)

def test_random_Title_default_length():
    result = random_Title()
    assert isinstance(result, str)
    assert 8 <= len(result) <= 14
    assert result[0].isupper()  # Check that the first letter is uppercase
    assert all(c in string.ascii_lowercase + string.digits + " " for c in result[1:])

def test_random_Title_custom_length():
    result = random_Title(min_length=10, max_length=20)
    assert isinstance(result, str)
    assert 10 <= len(result) <= 20
    assert result[0].isupper()  # Check that the first letter is uppercase
    assert all(c in string.ascii_lowercase + string.digits + " " for c in result[1:])
