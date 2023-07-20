# # import reqpy
# # import yaml
# # from yaml.loader import SafeLoader
# # from pathlib import Path


# # req1 = reqpy.requirements.Requirement(
# #     title="Toto toto toto",
# #     detail="sdf,sdf,s:,f:s,d:f;,sd:;f,sd:,f:,sdfsdgfdf:lmkbcvx:,bfvcx\ndsfsdkjfmlsdkfmldsklf\ndsfsdkfhskdhf\nsdlfsjdlkfjlsdjfldqs"
# # )

# # path = req1.write()

# # #path = Path("Toto_toto_toto.yml")


# # # Open the file and load the file
# # with open(path) as f:
# #     data = yaml.load(f, Loader=SafeLoader)
# #     req2 = reqpy.requirements.Requirement(**data)

# # print(req2)

# # print(dict(req2))

# # print(req2.toStrdict())

# from reqpy.requirements import Requirement
# from pathlib import Path


# a = Requirement(title='Bfgjldfgjlfkdjljg')


# # fp = a.write()
# fp = Path() / 'Bfgjldfgjlfkdjljg.yml'

# # a1 = Requirement.read(fp)

# # print(a1)

# # print(a1.is_valid_fileName(fp))

# print(Requirement.get_file_Errors(fp))

# print(a)
# print(a.listAttributes())

# # import reqpy

# # reqpy.generate_fakeDB(path=Path())


# # MDPath = Path() / "work" / "MD"

# # reqfolder = reqpy.folders.RequirementFolder(
# #     mainFolder=Path()
# # )

# # print(reqfolder)

# # reqfolder.generate_MD(MDPath=MDPath)

# a.toMDFile(
#     directoryPath=Path() / "titi"
# )


import reqpy
from pathlib import Path
import shutil

requirementPath = Path()
targetPath = Path()/"work"/"testMD"
outputPath = Path()/"work"/"site"

shutil.rmtree(targetPath, ignore_errors=True)
shutil.rmtree(outputPath, ignore_errors=True)

reqpy.build(
    projectTitle="Allez le SCO",
    targetPath=targetPath,
    outputPath=outputPath,
    requirementPath=requirementPath
)


from reqpy.mkdocs_utils import createMkDocsServer

createMkDocsServer(Path()/"work"/"testMD"/"mkdocs.yml")
