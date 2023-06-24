import reqpy
import pathlib
import logging




# req1 = reqpy.Requirement(
#     title="asfgfdfdg dfgdgtifd gghfdti",
#     detail="dfslfjksfjsdfj",
#     validation_status="valid"
# )

# filereq = reqpy.ReqFile(path ="toto.yaml")
# filereq.write(req1)
# print(filereq.get_valid_fileName())
# print(filereq.is_valid_fileName())

# aa = filereq.rename_file()

# print(filereq.path)

# print("allez")
# print(filereq.is_valid_fileName())

# os.remove(aa)

# reqpy.ReqFile(path = "reqDemo2.yaml").write(req1)

# req3 = reqpy.ReqFile(path = "reqDemo1.yaml").read()

# reqpy.ReqFile(path = "reqDemo_test.yaml").write(req3)

# req3 = reqpy.ReqFile(path = "reqDemo_test.yaml").read()
# print(req3)

# t = reqpy.utils.randomParagraph()
# print(t)

# logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger()
# reqpy.init_reqpy()    

# t = reqpy.ReqFolder(rootdir=pathlib.Path())
# t.create_dirs()


# print(t.get_missing_drectories())
# print(t.is_correct_folders())


# t.create_dirs()
# print(t.get_missing_drectories())
# print(t.is_correct_folders())

# print(t.get_list_of_files())
# print(t.get_incorrect_files())
# print(t.is_correct_files())

from reqpy.demo import generate_DB

generate_DB()

# from pathlib import Path

# req = reqpy.requirements.Requirement(
#     title="totodfgdfg",
#     detail="""
#     dgdslkjgdlsjgdflkjgldfjglkjdfj dlfjglkdfjlkdfjg dj  jdflgjdfljglkdfjg
#       lkdjfg  fdklfjgldf jglkdf lkjlk
#     """
# )

# req.write(folderPath=Path('work'))

# req2 = reqpy.requirements.Requirement.read(
#     Path("work/Totodfgdfg.yml")
# )

# print(reqpy.requirements.Requirement.get_file_Errors(Path("work/Totodfgdfg.yml")))

# rf = reqpy.requirements.ReqFile(path = "titi.yml")
# #rf.write(req)

# try:
#     req2 = rf.read()
# except Exception as e:
#     print(str(e))

