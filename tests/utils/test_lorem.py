import pytest
from reqpy.utils.__lorem_ipsum import TextLorem, randomSentence, randomParagraph, randomText

@pytest.fixture
def lorem_instance():
    """
    Fixture that creates an instance of TextLorem for testing.
    """
    return TextLorem()

def test_sentence_first_character_is_uppercase(lorem_instance):
    """
    Test that the first character of a generated sentence is uppercase.
    """
    sentence = lorem_instance.sentence()
    assert sentence[0].isupper()

def test_sentence_ends_with_period(lorem_instance):
    """
    Test that a generated sentence ends with a period.
    """
    sentence = lorem_instance.sentence()
    assert sentence.endswith('.')

def test_paragraph_contains_multiple_sentences(lorem_instance):
    """
    Test that a generated paragraph contains multiple sentences.
    """
    paragraph = lorem_instance.paragraph()
    assert paragraph.count('.') > 1

def test_text_contains_multiple_paragraphs(lorem_instance):
    """
    Test that a generated text contains multiple paragraphs.
    """
    text = lorem_instance.text()
    assert text.count('\n\n') > 1

def test_randomSentence_returns_string():
    """
    Test that randomSentence() returns a string.
    """
    sentence = randomSentence()
    assert isinstance(sentence, str)

def test_randomParagraph_returns_string():
    """
    Test that randomParagraph() returns a string.
    """
    paragraph = randomParagraph()
    assert isinstance(paragraph, str)

def test_randomText_returns_string():
    """
    Test that randomText() returns a string.
    """
    text = randomText()
    assert isinstance(text, str)
