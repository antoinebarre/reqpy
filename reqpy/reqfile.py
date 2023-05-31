""" Class used to handle the YAML files used to store requirement
"""

from pathlib import Path
from pydantic import BaseModel, validator
from .requirements import Requirement
from .__settings import RequirementFileSettings

class RefFile(BaseModel):
    path: Path

    # -------------------------- #
    @validator("path")
    def validate_extension(cls,value):
        path = Path(value)
        file_extension = path.suffix.lower()
        print(file_extension)
        if  (file_extension !="" and 
             file_extension in RequirementFileSettings.allowed_extensions):
            return value
        else:
            raise ValueError(
                f"The filepath {value} has not an appropriate extension " +
                f"i.e [{RequirementFileSettings.allowed_extensions}]"
            )
    # -------------------------- #
    def exists(self)-> bool:
        return self.path.exists()
    
    # -------------------------- #

    def read(self) :
        return True

    def write(self, req: Requirement):
        return True

    def delete(self):
        return True

    def create(self):
        return True
