""" tools used to handle string object in reqpy"""

import random
import string


__all__ = [
    "has_punctuation_or_accent",
    "generate_paragraph",
    "generate_title",
]


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

# ======================== LOREM ISPUM GENERATOR ======================== #


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
""".replace(".", "\n").split()

WORD_SEPARATOR = " "
SENTENCE_SEPARATOR = " "
PARAGRAPH_SEPARATOR = "\n\n"


def generate_paragraph(
            max_characters: int = 2000,
            ) -> str:
    """
    Generate a paragraph of Lorem Ipsum with a maximum number of characters.

    Args:
        max_characters (int): The maximum number of characters allowed in the generated paragraph.

    Returns:
        str: A randomly generated paragraph.

    Raises:
        ValueError: If max_characters is not strictly greater than 0.
    """
    if max_characters <= 0:
        raise ValueError('max number shall be strictly greater than 0')

    paragraph = ""
    for _ in range(random.randint(3, 200)):
        word = random.choice(DATA)
        paragraph += word + " "

        if len(paragraph) > max_characters:
            paragraph = paragraph[: max_characters - 3] + "..."
            break

    paragraph = paragraph[:-1] + "."
    return paragraph


def generate_title(
     min_characters: int,
     max_characters: int,
        ) -> str:
    """
    Generate a title with a random number of words and characters within the given limits.

    Args:
        min_characters (int): The minimum number of characters for the title.
        max_characters (int): The maximum number of characters for the title.

    Returns:
        str: A randomly generated title.

    Raises:
        ValueError: If min_characters is negative or if max_characters is less than min_characters.
    """
    if min_characters < 0:
        raise ValueError('min number shall be greater or equal to 0')

    if min_characters > max_characters:
        raise ValueError(
            ("max number of character"
             " shall be greater than the min"))

    max_characters = random.randint(min_characters, max_characters)

    title = ""
    for _ in range(random.randint(3, 200)):
        word = random.choice(DATA)
        title += word + " "

        if len(title) > max_characters:
            title = title[: max_characters]
            break

    def remove_non_alphanumeric(
            input_string: str
            ) -> str:
        return ''.join(char for char in input_string
                       if char.isalnum() or char.isspace())

    def capitalize_first_character(
            input_string: str
            ) -> str:
        return (
            input_string[0].upper() +
            input_string[1:]
        )

    return capitalize_first_character(
            remove_non_alphanumeric(title))


def random_string(
        min_length: int = 8,
        max_length: int = 14)-> str:
    """
    Get a random string
    Args:
        min_length: Minimal length of string
        max_length: Maximal length of string
    Returns:
        Random string of ascii characters
    """
    length = random.randint(min_length, max_length)
    return ''.join(
        random.choice(string.ascii_lowercase + string.digits + " ")
        for _ in range(length)
    )


def random_Title(
        min_length: int = 8,
        max_length: int = 14) -> str:
    """
    Get a random Title with a first capital letter
    Args:
        min_length: Minimal length of string
        max_length: Maximal length of string
    Returns:
        Random string of ascii characters
    """
    input_string = random_string(
        min_length=min_length,
        max_length=max_length)

    first_letter = random.choice(string.ascii_uppercase)

    return (first_letter +
            input_string[1:])