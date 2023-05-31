"""All settings needed by reqpy"""
# IMPORT MODULES
from typing import NamedTuple

# ########################################################################## #
# ######################### REQUIREMENTS PARAMETERS ######################## #
# ########################################################################## #

class RequirementSettings(NamedTuple):
    min_title_length = 8 # min size of the title
    max_title_length = 60 # max size of the title
    max_detail_length = 2000 # maximum size of the req description
    
class RequirementFileSettings(NamedTuple):
    allowed_extensions = (".yml",".yaml") # min size of the title
