"""Manage settings of the reqpy uses"""

from typing import NamedTuple


class RequirementSettings(NamedTuple):
    min_title_length = 8  # min size of the title
    max_title_length = 60  # max size of the title
    max_description_length = 2000  # maximum size of the req description