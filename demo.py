import reqpy
import pathlib


r = reqpy.validation.has_punctuation_or_accent("string ")



req1 = reqpy.Requirement(
    title="asfgfdfdgdfgdgtiti",
    detail="dfslfjksfjsdfj",
    validation_status="valid"
)


# reqpy.ReqFile(path = "reqDemo2.yaml").write(req1)

# req3 = reqpy.ReqFile(path = "reqDemo1.yaml").read()

# reqpy.ReqFile(path = "reqDemo_test.yaml").write(req3)

# req3 = reqpy.ReqFile(path = "reqDemo_test.yaml").read()
# print(req3)

t = reqpy.ReqFolder(rootdir=pathlib.Path())
t.create_dirs()
t.clean_dirs()