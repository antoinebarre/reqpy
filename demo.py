from pathlib import Path
import reqpy

a = reqpy.Requirement(
    title="Totoxcv dfg dfg vcxvxc"
)

print(a)

a.write(filePath=Path("titi.yml"))

b = reqpy.Requirement.read(filePath=Path("titi.yml"))
print(b)