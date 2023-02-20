import re
import math
from helpers import *

# Since this needs heleprs and num and sym, must be in its own file

def COL(n, s):
    # Our remade col class
    col = NUM(n, s) if re.search("^[A-Z]", s) else SYM(n, s)
    col["isIgnored"] = re.search("X$", col["txt"])
    col["isKlass"] = re.search("!$", col["txt"])
    col["isGoal"] = re.search("[!+-]$", col["txt"])
    return col

def NUM(n=0, s=""):
    # Our remade num class
    return {"at": n, "txt": s, "n": 0, "hi": -math.inf, "lo": math.inf, "ok": True, "isSym": False, "has": {}, "w": (-1 if re.search("-$", s) else 1)}

def SYM(n=0, s=""):
    # Our remade sym class
    return {"at": n, "txt": s, "n": 0, "mode": None, "most": 0, "isSym": True, "has": {}}

def COLS(ss):
    # Our remade cols class
    cols = {"names":ss, "all": {}, "x": {}, "y": {}}
    for n,s in ss.items():
        col = push(cols["all"], COL(n, s))
        if not col["isIgnored"]:
            if col["isKlass"]:
                cols["klass"] = col
            push((cols["y"] if col["isGoal"] else cols["x"]), col)
    return cols

def RANGE(at, txt, lo, hi=None):
    # New range class reformatted to be {}
    if hi is None:
        hi = lo
    return {"at": at, "txt":txt, "lo":lo, "hi":hi, "y": SYM()}

def DNEW():
    # The new method of DATA
    return {"rows": {}, "cols": None}

def DREAD(sfile):
    # The read method of DATA
    data = DNEW()
    csv(sfile, lambda t: row(data, t))
    return data

def DCLONE(data, ts={}):
    # The clone method of DATA
    data1 = row(DNEW(), data["cols"]["names"])
    for _, t in ts.items():
        row(data1, t)
    return data1

def row(data, t):
    # Our remade row class
    if data["cols"]:
        push(data["rows"], t)
        for _, cols in enumerate([data["cols"]["x"], data["cols"]["y"]]):
            for _, col in cols.items():
                add(col, t[col["at"]])
    else:
        data["cols"] = COLS(t)
    return data