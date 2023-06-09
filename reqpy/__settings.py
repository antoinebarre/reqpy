"""All settings needed by reqpy"""
# IMPORT MODULES
from typing import NamedTuple
from pathlib import Path

# ########################################################################## #
# ######################### REQUIREMENTS PARAMETERS ######################## #
# ########################################################################## #

class RequirementSettings(NamedTuple):
    min_title_length = 8 # min size of the title
    max_title_length = 60 # max size of the title
    max_detail_length = 2000 # maximum size of the req description
    validation_status = ("VALID","UNVALID","INVALID")
    
class RequirementFileSettings(NamedTuple):
    allowed_extensions = (".yml",".yaml") # min size of the title
    default_extension = ".yml" # default extension during file creation

class FolderStructure(NamedTuple):
    folder_structure =(
        "requirements",
        "requirements/lins",
        "requirements/info",  
    )
    
    # {
    #     'name':'requirements',
    #     'sub': [{
    #         'name':'links',
    #         'sub':[]
    #     },{
    #         'name':'analysis',
    #         'sub':[]
    #     }]
    # }
