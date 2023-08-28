"""Manage settings of the reqpy uses"""

from typing import NamedTuple


class RequirementSettings(NamedTuple):
    min_title_length = 8  # min size of the title
    max_title_length = 100  # max size of the title
    max_description_length = 2000  # maximum size of the req description


class DefinitionSettings(NamedTuple):
    min_title_length = 2  # min size of the title
    max_title_length = 100  # max size of the title
    max_description_length = 1000


class FoldersSettings(NamedTuple):
    main_folder_name = "SRS"
    requirements_folder_name = "requirements"
    references_folder_name = "references"
    definitions_folder_name = "definitions"
