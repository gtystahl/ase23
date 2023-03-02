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


  """
  def worker(rows, worse, above=None):
    if len(rows) < (len(data["rows"]) ** config.the["min"]):
      return rows, many(worse, config.the["rest"] * len(rows))
    else:
      # Changed this since there is no cols
      l, r, A, B, _ = half(data, rows, None, above)
      if better(data, B, A):
        ol = l
        l = r
        r = ol
        oa = A
        A = B
        B = oa
      MAP(r, lambda row: push(worse, row))
      return worker(l, worse, A)
  best, rest = worker(data["rows"], {})
  return DCLONE(data, best), DCLONE(data, rest)
  """


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
      return merges(ranges, n / config.the["bins"], config.the["d"] * div(col))
    
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


  """
  out = {}
  for _, col in cols.items():
    ranges = {}
    for y, rows in rowss.items():
      for _, row in rows.items():
        x = row[col["at"]]
        if x != "?":
          k = BIN(col, x)
          if not k in ranges.keys():
            ranges[k] = RANGE(col["at"], col["txt"], x)
          extend(ranges[k], x, y)
    def f(d):
      return d["lo"]
    ranges = sort(MAP(ranges, itself), f)
    out[len(out)] = lstToDict(ranges) if col["isSym"] else mergeAny(ranges)
  return out
  """


def BIN(col, x):
  # Returns what bin this item needs to be in
  if x == "?" or col["isSym"]:
    return x
  tmp = (col["hi"] - col["lo"]) / (config.the["bins"] - 1)
  return 1 if col["hi"] == col["lo"] else math.floor(x / tmp + 0.5) * tmp


def xpln(data):
  def v(has):
    return value(has, len(best["rows"]), len(rest["rows"]), "best")
  
  def score(ranges):
    rule = RULE(ranges, maxSizes)
    if rule:
      bestr = selects(rule, best["rows"])
      restr = selects(rule, rest["rows"])
      if len(bestr) + len(restr) > 0:
        return v({"best": len(bestr), "rest": len(restr)}), rule
  
  best, rest, evals = sway(data)
  tmp = {}
  maxSizes = {}
  for _, ranges in bins(data["cols"]["x"], {"best": best["rows"], "rest": rest["rows"]}).items():
    maxSizes[ranges[0]["txt"]] = len(ranges)
    for _, range in ranges.items():
      push(tmp, {"range": range, "max":len(ranges), "val":v(range["y"]["has"])})
  def f(d):
    return -d["val"]
  rule, most = firstN(sort(tmp, f), score)
  return best, rest, rule, most, evals


# A list is passed to the first parameter from above, be mindful
def firstN(sortedRanges, scoreFun):
  first = sortedRanges[0]["val"]
  def useful(range):
    if range["val"] > 0.5 and range["val"] > first / 10:
      return range
    
  # TODO Check the result of this. Based on my map, might be wonky
  sortedRanges = MAP(lstToDict(sortedRanges), useful)
  most = -1
  # TODO Might need to change this too
  def f(d):
    return d["range"]
  for n in range(0, len(sortedRanges)):
    tmp, rule = None, None
    res = scoreFun(MAP(SLICE(sortedRanges, 0, n), f))
    if res:
      tmp = res[0]
      rule = res[1]
    if tmp and tmp > most:
      out = rule
      most = tmp
  return out, most


def showRule(rule):
  def pretty(range):
    return range["lo"] if range["lo"] == range["hi"] else {0: range["lo"], 1: range["hi"]}
  def f(d):
    return d["lo"]
  def merges(attr, ranges):
    return MAP(merge(lstToDict(sort(ranges, f))), pretty)
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
    return merges(k, v), None
  return kap(rule, altMerges)


def selects(rule, rows):
  def oneOfThem(ranges, row):
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
  
  def allOfThem(row):
    for _, ranges in rule.items():
      if not oneOfThem(ranges, row):
        return False
    return True
  
  return MAP(rows, lambda r: r if allOfThem(r) else None)