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
        if not col["isIgnored"] and col["isKlass"]:
                cols["klass"] = col
        if not col["isIgnored"]:
            push((cols["y"] if col["isGoal"] else cols["x"]), col)
    return cols


def RANGE(at, txt, lo, hi=None):
    # New range class reformatted to be {}
    if hi is None:
        hi = lo
    return {"at": at, "txt":txt, "lo":lo, "hi":hi, "y": SYM()}


def RULE(ranges, maxSize):
    # This generates a rule for the xpln function in comboFuncs.py
    t = {}
    for _, range in ranges.items():
        if not range["txt"] in t.keys():
            t[range["txt"]] = {}
        push(t[range["txt"]], {"lo": range["lo"], "hi": range["hi"], "at": range["at"]})
    return prune(t, maxSize)


def prune(rule, maxSize):
    # Prunces rules that are too generic (aka tries to cover everything)
    n = 0
    for txt, ranges in rule.items():
        n = n + 1
        if len(ranges) == maxSize[txt]:
            n = n + 1
            rule[txt] = None
        if n > 0:
            return rule


def DATA(src, rows={}):
    # Remade remade data which includes read and clone inside of it
    data = {"rows": {}, "cols": None}
    add = lambda t: row(data, t)
    if type(src) == str:
        csv(src, add)
    else:
        data["cols"] = COLS(src["cols"]["names"])
    MAP(rows, add)
    return data


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