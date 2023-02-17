from newClasses import *
from newHelpers import *

# This file holds all of the functions that require the helpers and the classses

def tree(data, rows=None, cols=None, above=None):
  if rows is None:
    rows = data["rows"]
  here = {"data": DCLONE(data, rows)}
  if len(rows) >= 2 * (len(data["rows"])) ** config.the["min"]:
    left, right, A, B, _ = half(data, rows, cols, above)
    here["left"] = tree(data, left, cols, A)
    here["right"] = tree(data, right, cols, B)
  return here


def showTree(tree, lvl=0, post=None):
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
  def worker(rows, worse, above=None):
    if len(rows) <= (len(data["rows"]) ** config.the["min"]):
      return rows, many(worse, config.the["rest"] * len(rows))
    else:
      # Changed this since there is no cols
      l, r, A, B, _ = half(data, rows, None, above)
      if better(data, B, A):
        l, r, A, B = r, l, B, A
      MAP(r, lambda row: push(worse, row))
      return worker(l, worse, A)
  best, rest = worker(data["rows"], {})
  return DCLONE(data, best), DCLONE(data, rest)


def bins(cols, rowss):
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
    ranges = sort(MAP(ranges, itself), lo)
    out[1 + len(out)] = ranges if col["isSym"] else mergeAny(ranges)
  return out


def bin(col, x):
  if x == "?" or col["isSym"]:
    return x
  tmp = (col["hi" - col["lo"]]) / (config.the["bins"] - 1)
  return 1 if col["hi"] == col["hi"] else math.floor(x / tmp + 0.5) * tmp


