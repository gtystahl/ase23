import re

s = "false"

res = re.match("^\s*(.+)\s*$", s)
# res = re.match("(.)", s)
# res = re.search("(.+)", s)

res2 = "hello"
res2 = res2[1:2]
print("done")