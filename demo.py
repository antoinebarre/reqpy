import reqpy


r = reqpy.validation.has_punctuation_or_accent("string ")

print(r)

req1 = reqpy.Requirement(
    title="asfgfdfdgdfgdg.titi",
    detail="dfslfjksfjsdfj",
    validation_status="valid"
)
print(req1)

# reqpy.ReqFile(path = "reqDemo2.yaml").write(req1)

# req3 = reqpy.ReqFile(path = "reqDemo1.yaml").read()

# reqpy.ReqFile(path = "reqDemo_test.yaml").write(req3)

# req3 = reqpy.ReqFile(path = "reqDemo_test.yaml").read()
# print(req3)