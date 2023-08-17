"""tools developed for the string handling"""

import re
import string
import random

__all__ = [
    "has_punctuation_or_accent",
    "generate_paragraph",
    "generate_sentence",
    'randomParagraph',
    'randomSentence',
    "randomText",
    "generate_random_string",
]


# ============================= STRING TOOLS ============================ #

def has_punctuation_or_accent(text: str) -> bool:
    """
    Checks if a string contains punctuation characters or accents.

    Args:
        text (str): The input string to check.

    Returns:
        bool: True if the string contains punctuation characters
        or accents, False otherwise.

    """
    punctuation_chars = set(string.punctuation)
    for char in text:
        if char in punctuation_chars or (not char.isascii()):
            return True
    return False


""" LOREM ISPUM MODULE TO GENERATE RANDOM TEXT"""


# list of possibles words
DATA = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam placerat
mauris ut est ultricies, ut iaculis ipsum cursus. Pellentesque venenatis
viverra augue id venenatis. Mauris suscipit nunc non ipsum commodo ultrices.
Curabitur cursus rhoncus sapien, at cursus odio. Nullam eleifend, neque vitae
consequat tincidunt, justo massa auctor nisl, vitae ullamcorper mi metus sed
risus. Donec maximus orci sed laoreet ultricies. Etiam malesuada lacus sit
amet felis interdum efficitur. Vestibulum sagittis leo et mauris dapibus
congue. Integer luctus justo odio, ut bibendum velit aliquet non. In feugiat
a mi eu euismod. Nam dapibus nunc eu ex congue, nec tincidunt sapien vulputate.
Donec congue odio mi, a laoreet massa tincidunt id. Nulla at tincidunt metus.
Cras sit amet velit at purus gravida elementum a nec libero. Morbi malesuada
nulla nec dui efficitur ultricies. Sed ultricies dictum arcu a efficitur.
Vestibulum ac ex eget massa convallis dignissim at at nisl. Mauris tristique
velit at ultricies dictum. Curabitur dignissim tincidunt mi, sit amet congue
mi fermentum vitae. Nullam ut aliquam dolor. Sed in orci ut sem sollicitudin
posuere eu non libero. Nam ut sem eu felis luctus finibus. In hac habitasse
platea dictumst. Aenean interdum libero ac quam iaculis, id ultrices nunc
tempor. Suspendisse varius dui a sem gravida, vel interdum ligula commodo.
Curabitur venenatis tortor non odio gravida, non rutrum metus congue. Nulla
aliquet aliquam tincidunt. Nullam congue feugiat dui at tempus.
Quisque interdum auctor risus, in venenatis neque tincidunt sed.
Nullam interdum elit in fringilla facilisis. Suspendisse fermentum auctor
libero ut vulputate. Pellentesque efficitur, lectus in semper hendrerit,
justo ligula vestibulum purus, in dapibus felis purus et metus. Morbi dapibus
convallis finibus. Nullam ut enim eget nisl efficitur luctus in at augue. Ut
auctor elementum sapien, sit amet consequat ex tempus non. Curabitur lobortis
metus id elit lobortis, sit amet facilisis dui congue. Sed eget rutrum elit.
Aliquam mollis dictum fringilla. Donec ac tellus eget magna placerat mattis.
Vivamus fringilla, felis nec rhoncus varius, neque nisi iaculis libero, non
fringilla nunc purus non tortor. Quisque varius libero vitae ante lobortis
vestibulum. Nulla facilisi.
Mauris ultricies tortor vitae orci luctus, ac dignissim justo consequat.
Sed viverra scelerisque scelerisque. Donec posuere interdum neque, in
vestibulum neque viverra et. Mauris vitae tellus lobortis, tristique arcu ege,
fermentum nisl. Nam vel
""".replace(".", "").split()

WORD_SEPARATOR = " "
SENTENCE_SEPARATOR = " "
PARAGRAPH_SEPARATOR = "\n\n"


def generate_paragraph(
            max_characters: int = 2000,
            ) -> str:
    """
    Generate a paragraph of Lorem Ipsum with a maximum number of characters.

    Args:
        max_characters (int): The maximum number of characters allowed in the
                                generated paragraph.

    Returns:
        str: A randomly generated paragraph.
    """
    paragraph = ""
    for _ in range(random.randint(3, 200)):
        word = random.choice(DATA)
        paragraph += word + " "

        if len(paragraph) > max_characters:
            paragraph = paragraph[: max_characters - 3] + "..."
            break

    paragraph = paragraph[:-1] + "."
    return paragraph


def generate_sentence(
        max_characters: int = 100,
        only_alphanum: bool = False,
        ) -> str:
    sentence = ""

    for _ in range(random.randint(3, 20)):
        word = random.choice(DATA)
        sentence += word + " "

        if len(sentence) > max_characters:
            sentence = sentence[: max_characters]
            break

    sentence = sentence[0].upper() + sentence[1:]

    if only_alphanum:
        pattern = re.compile(r"[^a-zA-Z0-9 ]")
        return pattern.sub("", sentence)
    else:
        sentence = sentence[:-1] + "."
        return sentence


class TextLorem():
    """
    Lorem Ipsum text generator.

    Attributes:
        _srange (tuple): A tuple representing the range of sentence lengths.
        _prange (tuple): A tuple representing the range of paragraph lengths.
        _trange (tuple): A tuple representing the range of text lengths.
        _words (list): A list of words used for generating text.

    Methods:
        sentence(): Generates a random sentence.
        paragraph(): Generates a random paragraph.
        text(): Generates a random text.
        _word(): Returns a random word from the word list.
    """
    def __init__(self, srange=(4, 8), prange=(5, 10), trange=(3, 6)):
        """
        Initialize the TextLorem instance.

        Args:
            srange (tuple): A tuple representing the range of sentence lengths.
                Default is (4, 8).
            prange (tuple): A tuple representing the range of paragraph
                            lengths.
                Default is (5, 10).
            trange (tuple): A tuple representing the range of text lengths.
                Default is (3, 6).
        """
        self._srange = srange
        self._prange = prange
        self._trange = trange
        self._words = DATA

    def sentence(self):
        """
        Generate a random sentence.

        Returns:
            str: A randomly generated sentence.
        """
        n = random.randint(*self._srange)
        s = WORD_SEPARATOR.join(self._word() for _ in range(n))
        return s[0].upper() + s[1:] + '.'

    def paragraph(self):
        """
        Generate a random paragraph.

        Returns:
            str: A randomly generated paragraph.
        """
        n = random.randint(*self._prange)
        p = SENTENCE_SEPARATOR.join(self.sentence() for _ in range(n))
        return p

    def text(self):
        """
        Generate a random text.

        Returns:
            str: A randomly generated text.
        """
        n = random.randint(*self._trange)
        t = PARAGRAPH_SEPARATOR.join(self.paragraph() for _ in range(n))
        return t

    def _word(self):
        """
        Return a random word from the word list.

        Returns:
            str: A randomly selected word.
        """
        return random.choice(self._words)


def randomSentence(*args, **kwargs):
    """
    Generate a random sentence using default settings.

    Returns:
        str: A randomly generated sentence.
    """
    return TextLorem().sentence(*args, **kwargs)


def randomParagraph(*args, **kwargs):
    """
    Generate a random paragraph using default settings.

    Returns:
        str: A randomly generated paragraph.
    """
    return TextLorem().paragraph(*args, **kwargs)


def randomText(*args, **kwargs):
    """
    Generate a random paragraph using default settings.

    Returns:
        str: A randomly generated paragraph.
    """
    return TextLorem().text(*args, **kwargs)


def generate_random_string(size: int) -> str:
    """
    Generate a random string with alphanumeric characters and spaces.

    Args:
        size (int): The desired size of the string.

    Returns:
        str: The randomly generated string.

    Raises:
        ValueError: If the size argument is less than or equal to 0.
    """
    if size <= 0:
        raise ValueError("Size argument must be greater than 0.")

    # Choose a random character from alphanumeric characters and spaces
    first_char = random.choice(string.ascii_letters)
    remaining_chars = ''.join(
        random.choices(string.ascii_letters + string.digits + " ", k=size - 1)
        )

    return first_char + remaining_chars
