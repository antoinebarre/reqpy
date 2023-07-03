# from reqpy.RequirementItems import RequirementRationale
# from reqpy.requirements import Requirement
# from pathlib import Path


# a = RequirementRationale("dfsdfs")
# print(a)

# b = Requirement(title='Tititidfgddfg')
# b.write()

# c = Requirement.read(filePath=Path('Tititidfgddfg.yml'))
# print(c)

# import reqpy

# a = reqpy.validate_reqpy_database()

# from reqpy.__logging import printConsole

# printConsole(message="toto", type="titi")

import reqpy
from pathlib import Path

reqpy.generate_fakeDB()