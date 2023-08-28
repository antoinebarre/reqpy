from pathlib import Path
from reqpy import Apps
from reqpy import Requirement, RequirementsSet
import shutil


a = Requirement.createFakeRequirement()

mySRS = Path("work/SRS")
myReport = Path("work/report/requirements")

shutil.rmtree(mySRS, ignore_errors=True)
shutil.rmtree(myReport, ignore_errors=True)
mySRS.mkdir(exist_ok=True, parents=True)
myReport.mkdir(exist_ok=True, parents=True)

# b = RequirementsSet(mySRS)

#b.createFakeRequirementsSet()


# b.generateMD(myReport,show_console=True)

# df = b.toPandas()
# df.head()


a = Apps(rootDir=mySRS)

a.initiate_database(show_console=True)

a.reset_database(show_console=True)

a.create_new_requirement(show_console=True)

a.create_fake_database(show_console=True)
