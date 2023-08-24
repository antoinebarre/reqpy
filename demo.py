from pathlib import Path
from reqpy import Requirement

a = Requirement.createFakeRequirement()
print(a.toMD())