""" tools used to handle string object in reqpy"""

import string


__all__ = [
    "has_punctuation_or_accent",
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
