import reqpy

req1 = reqpy.Requirement(
    title="asfgfdfdgdfgdg",
    content="dfslfjksfjsdfj"
)


print(req1)

reqfile = reqpy.RefFile(path="toto.yml")
print(reqfile.exists())

req2 = reqpy.Requirement()
print(req2)
