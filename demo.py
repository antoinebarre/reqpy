from reqpy.tools.status import CheckStatus

a1 = CheckStatus(valid=True, message=["ghffghfg"])
print(a1)

a2 = CheckStatus(valid=False, message=["dfgfdlkg,dfl,g:df;,g:;df,g,d"])
print(a2)

a3 = a1 + a2

print(a3+a2)

