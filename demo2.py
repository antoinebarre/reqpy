from pathlib import Path
from reqpy.definition import Definition


a = Definition(title="SCO")

newfile = Path("work/def/def101.yml")

b = Definition.read(filePath=newfile)


print(b.get_all_occurences())

print(b.validateDefinitionFile(newfile).tostr())