import reqpy
import pathlib
import os



req1 = reqpy.Requirement(
    title="asfgfdfdg dfgdgtifd gghfdti",
    detail="dfslfjksfjsdfj",
    validation_status="valid"
)

filereq = reqpy.ReqFile(path ="toto.yaml")
filereq.write(req1)
print(filereq.get_valid_fileName())
print(filereq.is_valid_fileName())

aa = filereq.rename_file()

print(filereq.path)

print("allez")
print(filereq.is_valid_fileName())

os.remove(aa)

# reqpy.ReqFile(path = "reqDemo2.yaml").write(req1)

# req3 = reqpy.ReqFile(path = "reqDemo1.yaml").read()

# reqpy.ReqFile(path = "reqDemo_test.yaml").write(req3)

# req3 = reqpy.ReqFile(path = "reqDemo_test.yaml").read()
# print(req3)

t = reqpy.ReqFolder(rootdir=pathlib.Path())
t.create_dirs()
t.clean_dirs()