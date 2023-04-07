# NOTE Should be left alone since it wasn't combined. However, may be broke
from classes import *
from helpers import *
import config

# This file holds all of the functions that require the helpers and the classses

def tree(data, rows=None, cols=None, above=None):
  # Creates a tree of the data 
  if rows is None:
    rows = data["rows"]
  here = {"data": DATA(data, rows)}
  if len(rows) >= 2 * (len(data["rows"])) ** config.the["min"]:
    left, right, A, B, _, _ = half(data, rows, cols, above)
    here["left"] = tree(data, left, cols, A)
    here["right"] = tree(data, right, cols, B)
  return here


def showTree(tree, lvl=0, post=None):
  # Prints the created tree to the screen
  if tree:
    line = ""
    for i in range(lvl):
      line += "|.."
    print("%s[%s]" % (line, len(tree["data"]["rows"])), end=" ")
    if (lvl == 0) or (not "left" in tree.keys()):
      print(stats(tree["data"]))
    else:
      print("")
    
    if not "left" in tree.keys():
      showTree(None, lvl+1)
    else:
      showTree(tree["left"], lvl+1)

    if not "right" in tree.keys():
      showTree(None, lvl+1)
    else:
      showTree(tree["right"], lvl+1)


def sway(data):
  # Our optimized clustering algorithm sway
  def worker(rows, worse, evals0, above=None):
    if len(rows) < (len(data["rows"]) ** config.the["min"]):
      return rows, many(worse, config.the["rest"] * len(rows)), evals0
    else:
      l, r, A, B, c, evals = half(data, rows, None, above)
      if better(data, B, A):
        ol = l
        l = r
        r = ol
        oa = A
        A = B
        B = oa
      MAP(r, lambda row: push(worse, row))
      return worker(l, worse, evals + evals0, A)
  best, rest, evals = worker(data["rows"], {}, 0)
  return DATA(data, best), DATA(data, rest), evals


def bins(cols, rowss):
  # Seperates the data into bins
  def with1Col(col):
    n, ranges = withAllRows(col)
    def f(d):
      return d["lo"]
    ranges = sort(MAP(ranges, itself), f)
    if col["isSym"]:
      return lstToDict(ranges)
    else:
      res = merges(ranges, n / config.the["bins"], config.the["d"] * div(col))
      return lstToDict(res)
    
  def withAllRows(col):
    global nvar
    nvar = 0
    ranges = {}
    def xy(x,y):
      global nvar
      if x != "?":
        nvar = nvar + 1
        k = BIN(col, x)
        if not k in ranges.keys():
          ranges[k] = RANGE(col["at"], col["txt"], x)
        extend(ranges[k], x, y)

    for y, rows in rowss.items():
      for _, row in rows.items():
        xy(row[col["at"]], y)
    return nvar, ranges

  return MAP(cols, with1Col)


def BIN(col, x):
  # Returns what bin this item needs to be in
  if x == "?" or col["isSym"]:
    return x
  tmp = (col["hi"] - col["lo"]) / (config.the["bins"] - 1)
  return 1 if col["hi"] == col["lo"] else math.floor(x / tmp + 0.5) * tmp


def xpln(data, best, rest):
  # A cluster based on rules instead of values to show which parts are important
  def v(has):
    return value(has, len(best["rows"]), len(rest["rows"]), "best")
  
  def score(ranges):
    rule = RULE(ranges, maxSizes)
    if rule:
      prettyPrint(showRule(rule), 1)
      bestr = selects(rule, best["rows"])
      restr = selects(rule, rest["rows"])
      if len(bestr) + len(restr) > 0:
        return v({"best": len(bestr), "rest": len(restr)}), rule

  tmp = {}
  maxSizes = {}
  for _, ranges in bins(data["cols"]["x"], {"best": best["rows"], "rest": rest["rows"]}).items():
    maxSizes[ranges[0]["txt"]] = len(ranges)
    print("")
    for _, range in ranges.items():
      print(range["txt"], range["lo"], range["hi"])
      push(tmp, {"range": range, "max":len(ranges), "val":v(range["y"]["has"])})
  def f(d):
    return -d["val"]
  rule, most = firstN(lstToDict(sort(tmp, f)), score)
  return rule, most


def firstN(sortedRanges, scoreFun):
  # This gets the useful rules made above
  print("")
  MAP(sortedRanges, lambda r: print(r["range"]["txt"], r["range"]["lo"], r["range"]["hi"], rnd(r["val"]), r["range"]["y"]["has"]))
  first = sortedRanges[0]["val"]
  def useful(range):
    if range["val"] > 0.05 and range["val"] > first / 10:
      return range
    
  sortedRanges = MAP(lstToDict(sortedRanges), useful)
  most = -1
  out = -1
  def f(d):
    return d["range"]
  for n in range(0, len(sortedRanges)):
    tmp, rule = None, None
    res = scoreFun(MAP(SLICE(sortedRanges, 0, n + 1), f))
    if res:
      tmp = res[0]
      rule = res[1]
    if tmp and tmp > most:
      out = rule
      most = tmp
  return out, most


def showRule(rule):
  # Prints the rules to the screen
  def pretty(range):
    return range["lo"] if range["lo"] == range["hi"] else {0: range["lo"], 1: range["hi"]}
  def f(d):
    return d["lo"]
  def merges(attr, ranges):
    return MAP(merge(lstToDict(sort(ranges, f))), pretty), attr
  def merge(t0):
    t = {}
    j = 0
    while j < len(t0):
      left = t0[j]
      right = None
      try:
        right = t0[j + 1]
      except:
        pass
      
      if right and left["hi"] == right["lo"]:
        left["hi"] = right["hi"]
        j = j + 1
      push(t, {"lo": left["lo"], "hi": left["hi"]})
      j = j + 1
    return t if len(t0) == len(t) else merge(t)
  def altMerges(k, v):
    return merges(k, v)
  return kap(rule, altMerges)


def selects(rule, rows):
  # Selects the best rule that works for all
  def disjunction(ranges, row):
    for _, range in ranges.items():
      lo = range["lo"]
      hi = range["hi"]
      at = range["at"]
      x = row[at]
      if x == "?":
        return True
      if lo == hi and lo == x:
        return True
      if lo <= x and x < hi:
        return True
    return False
  
  def conjunction(row):
    for _, ranges in rule.items():
      if not disjunction(ranges, row):
        return False
    return True
  
  return MAP(rows, lambda r: r if conjunction(r) else None)