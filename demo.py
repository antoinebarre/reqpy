from pathlib import Path
from reqpy import Requirement, RequirementsSet
import shutil


a = Requirement.createFakeRequirement()
print(a.toMD())

mySRS = Path("work/SRS/requirements")
myReport = Path("work/report/requirements")

shutil.rmtree(mySRS, ignore_errors=True)
shutil.rmtree(myReport,ignore_errors=True)
mySRS.mkdir(exist_ok=True,parents=True)
myReport.mkdir(exist_ok=True,parents=True)

b = RequirementsSet(mySRS)

b.createFakeRequirementsSet()


b.generateMD(myReport,show_console=True)
