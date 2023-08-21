from reqpy.tools.status import CheckStatus, CheckStatusList

a= CheckStatus(check="c1",valid=True,message="")
b = CheckStatus(check="c2",valid=False,message="dfmlgkmlfgkmfld")

tt =CheckStatusList([a,b])

print(tt.is_valid())