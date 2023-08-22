from pathlib import Path
from reqpy.__DB import GenericDB
import shutil

a = GenericDB(folderPath=Path(),allowAdditionalFiles=True,allowSubfolders=True)

print(a.validateDataBase().is_valid())

from reqpy.requirement import RequirementsSet


folder = Path("work/toto")

shutil.rmtree(folder,ignore_errors=True)
folder.mkdir(exist_ok=True)

req = RequirementsSet(
    RequirementPath=folder)

req.createFakeRequirementsSet()
