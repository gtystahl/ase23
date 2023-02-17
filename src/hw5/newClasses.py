import re
import math
from newHelpers import *

# Since this needs heleprs and num and sym, must be in its own file

def COL(n, s):
    col = NUM(n, s) if re.search("^[A-Z]", s) else SYM(n, s)
    col["isIgnored"] = re.search("X$", col["txt"])
    col["isKlass"] = re.search("!$", col["txt"])
    col["isGoal"] = re.search("[!+-]$", col["txt"])
    return col

def NUM(n=0, s=""):
    return {"at": n, "txt": s, "n": 0, "hi": -math.inf, "lo": math.inf, "ok": True, "isSym": False, "has": {}, "w": (-1 if re.search("-$", s) else 1)}

def SYM(n=0, s=""):
    return {"at": n, "txt": s, "n": 0, "mode": None, "most": 0, "isSym": True, "has": {}}

def COLS(ss):
    cols = {"names":ss, "all": {}, "x": {}, "y": {}}
    for n,s in ss.items():
        col = push(cols["all"], COL(n, s))
        if not col["isIgnored"]:
            if col["isKlass"]:
                cols["klass"] = col
            push((cols["y"] if col["isGoal"] else cols["x"]), col)
    return cols

def RANGE(at, txt, lo, hi):
    # Might need to change the "hi" part
    return {"at": at, "txt":txt, "lo":lo, "hi":hi, "y": SYM()}

def DNEW():
    return {"rows": {}, "cols": None}

def DREAD(sfile):
    data = DNEW()
    csv(sfile, lambda t: row(data, t))
    return data

def DCLONE(data, ts={}):
    data1 = row(DNEW(), data["cols"]["names"])
    for _, t in ts.items():
        row(data1, t)
    return data1

def row(data, t):
    if data["cols"]:
        push(data["rows"], t)
        for _, cols in enumerate([data["cols"]["x"], data["cols"]["y"]]):
            for _, col in cols.items():
                add(col, t[col["at"]])
    else:
        data["cols"] = COLS(t)
    return data