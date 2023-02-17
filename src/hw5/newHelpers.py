import math
import sys
import re
import config
import os
import copy
import re
from pathlib import Path


"""
def csv(sFilename, fun):
  # Opens the csv file sFilename and runs the function fun on what is found in the csv
  file_path = Path(sFilename)
  file_path = file_path.absolute()
  file_path = file_path.resolve()
  f = open(file_path, "r")
  rl = f.readlines()
  f.close()
  for line in rl:
    t = []
    for s1 in re.findall("([^,]+)", line):
      t.append(coerce(s1))
    fun(t)
"""


def lstToDict(lst):
  d = {}
  for i in range(len(lst)):
    d[i] = lst[i]
  return d

def coerce(s):
  # Convert to python data types from strings
  def fun(s1):
    if s1 == "true" or s1 == "True":
      return True
    elif s1 == "false" or s1 == "False":
      return False
    else:
      return s1
  if type(s) == bool:
    return s
  try:
    res = int(s)
  except:
    try:
      res = float(s)
    except:
      res = fun(re.match("^\s*(.+)\s*$", s).string)
  return res


def add(col, x, n=1):
  if x != "?":
    col["n"] = col["n"] + n
    if col["isSym"]:
      val = 0
      if x in col["has"].keys():
        val = col["has"][x]
      col["has"][x] = n + val
      if col["has"][x] > col["most"]:
        col["most"] = col["has"][x]
        col["mode"] = x
    else:
      col["lo"] = min(x, col["lo"])
      col["hi"] = max(x, col["hi"])
      all = len(col["has"])
      pos = (all + 1 if all < config.the["Max"] else (rint(1, all) if rand() < config.the["Max"] / col["n"] else None)) 
      if pos is not None:
        col["has"][pos] = x
        col["ok"] = False


def rint(lo=0, hi=1):
  # This gets a random integer between the high and low
  return math.floor(0.5 + rand(lo, hi))


def rand(lo=0, hi=1):
  # Gets a random number between the high and low numbers
  config.Seed = (16807 * config.Seed) % 2147483647
  return lo + (hi - lo) * config.Seed / 2147483647


def adds(col, t={}):
  for _, x in t.items():
    add(col, x)
  return col


def extend(range, n, s):
  range["lo"] = min(n, range["lo"])
  range["hi"] = max(n, range["hi"])
  add(range["y"], s)


def has(col):
  if not col["isSym"] and not col["ok"]:
    col["has"] = lstToDict(sort(col["has"]))
  col["ok"] = True
  return col["has"]


def sort(t, fun=None):
  nt = []
  for k in t.keys():
    nt.append(t[k])
  if fun is not None:
    nt.sort(key=fun)
  else:
    nt.sort()

  return nt


def mid(col):
  return col["mode"] if col["isSym"] else per(has(col), .5)


def div(col):
  if col["isSym"]:
    e = 0
    for _, n in col["has"].items():
      e = e - n / col["n"] * math.log(n / col["n"], 2)
    return e
  else:
    return (per(has(col), .9) - per(has(col), .1)) / 2.58
  

def stats(data, fun=mid, cols=None, nPlaces=0):
  def f(k, col):
    return rnd(fun(col), nPlaces), col["txt"]
  
  if cols is None:
    cols = data["cols"]["y"]
  tmp = kap(cols, f)
  tmp["N"] = len(data["rows"])
  return tmp, MAP(cols, mid)


def MAP(t, fun):
  # This maps function fun over items in t
  u = {}
  if 0 in t.keys():
    for i in range(len(t)):
      k = i
      v = t[i]
      res = fun(v)
      if res is not None:
        u[len(u)] = res
  else:
    for k, v in t.items():
      res = fun(v)
      if res is not None:
        u[len(u)] = res
  return u


def kap(t, fun):
  # Like map but requires fun to be fun(k, v) not just v
  u = {}
  if 0 in t.keys():
    for i in range(len(t)):
      k = i
      v = t[i]
      v, k = fun(k, v)
      if k is not None:
        u[k] = v
      else:
        u[len(u)] = v
  else:
    for k, v in t.items():
      v, k = fun(k, v)
      if k is not None:
        u[k] = v
      else:
        u[len(u)] = v
  return u


def rnd(n, nPlaces=0):
  # Returns n rounded to the nPlaces
  mult = 0
  if nPlaces:
    mult = 10 ** nPlaces
  else:
    mult = 10 ** 3

  return math.floor(n * mult + 0.5) / mult


def norm(num, n):
  # I changed the xs to ns because I am not sure where the x comes from...
  return n if str(n) == "?" else (n - num["lo"])/(num["hi"] - num["lo"] + 1/math.inf)


def value(has, nB=1, nR=1, sGoal=True):
  b = 0
  r = 0
  for x, n in has.items():
    if x == sGoal:
      b = b + n
    else:
      r = r + n
  b = b/(nB+1/math.inf)
  r = r/(nR+1/math.inf)
  return b^2 / (b+r)


def dist(data, t1, t2, cols=None):
  def dist1(col, x, y):
    if x == "?" and y == "?":
      return 1
    if col["isSym"]:
      return 0 if x == y else 1
    else:
      x = norm(col, x)
      y = norm(col, y)
      if x == "?":
        # This and the other seems redundant because they both return the same?
        x = 1 if y < 0.5 else 1
      if y == "?":
        y = 1 if x < 0.5 else 1
      return abs(x - y)
    
  d = 0
  n = 1 / math.inf
  if cols is None:
    cols = data["cols"]["x"]
  for _, col in cols.items():
    n = n + 1
    d = d + dist1(col, t1[col["at"]], t2[col["at"]]) ** config.the["p"]
  return (d/n) ** (1/config.the["p"])


def better(data, row1, row2):
  s1 = 0
  s2 = 0
  ys = data["cols"]["y"]
  for _, col in ys.items():
    x = norm(col, row1[col["at"]])
    y = norm(col, row2[col["at"]])
    s1 = s1 - math.exp(col["w"] * (x - y)/len(ys))
    s2 = s2 - math.exp(col["w"] * (y - x)/len(ys))
  return s1 / len(ys) < s2 / len(ys)


def half(data, rows=None, cols=None, above=None):
  left = {}
  right = {}
  def gap(r1, r2):
    return dist(data, r1, r2, cols)
  def cos(a, b, c):
    return (a ** 2 + c ** 2 - b ** 2) / (2 * c)
  def proj(r):
    return {"row": r, "x": cos(gap(r, A), gap(r, B), c)}
  
  if rows is None:
    rows = data["rows"]
  some = many(rows, config.the["Halves"])
  A = above if config.the["Reuse"] and above else ANY(some)

  def f(d):
    return d["d"]
  tmp = sort(MAP(some, lambda r: {"row": r, "d": gap(r, A)}), f)
  far = tmp[int(len(tmp) * config.the["Far"])]
  B = far["row"]
  c = far["d"]

  def f(d):
    return d["x"]
  for n, two in enumerate(sort(MAP(rows, proj), f)):
    push(left if n < len(rows)/2 else right, two["row"])
  return left, right, A, B, c


def mergeAny(ranges0):
  def noGaps(t):
    for j in range(1, len(t)):
      t[j]["lo"] = t[j - 1]["hi"]
    t[0]["lo"] = -math.inf
    t[len(t) - 1]["hi"] = math.inf
    return t
  ranges1 = {}
  j = 0
  while j < len(ranges0):
    left = ranges0[j]
    right = None
    try:
      right = ranges0[j + 1]
    except:
      pass
    if right:
      y = merge2(left["y"], right["y"])
      if y:
        j = j + 1
        left["hi"], left["y"] = right["hi"], y
    push(ranges1, left)
    j = j + 1
  return noGaps(ranges0) if len(ranges0) == len(ranges1) else mergeAny(ranges1)


def merge2(col1, col2):
  new = merge(col1, col2)
  if div(new) <= (div(col1)*col1["n"] + div(col2)*col2["n"]) / new["n"]:
    return new
  

def merge(col1, col2):
  new = copy.deepcopy(col1)
  if col1["isSym"]:
    for x, n in col2["has"].items():
      add(new, x, n)
  else:
    for _, n in col2["has"].items():
      add(new, n)
      new["lo"] = min(col1["lo"], col2["lo"])
      new["hi"] = max(col1["hi"], col2["hi"])
  return new


def itself(x): return x


def cliffDelta(ns1, ns2):
  if len(ns1) > 256:
    ns1 = many(ns1, 256)
  if len(ns2) > 256:
    ns2 = many(ns2, 256)
  if len(ns1) > 10 * len(ns2):
    ns1 = many(ns1, 10 * len(ns2))
  if len(ns2) > 10 * len(ns1):
    ns2 = many(ns2, 10 * len(ns1))
  n = 0
  gt = 0
  lt = 0
  for _, x in ns1.items():
    for _, y in ns2.items():
      n = n + 1
      if x > y:
        gt = gt + 1
      if x < y:
        lt = lt + 1
  # print(abs(lt - gt) / n)
  # print(config.the["cliffs"])
  return abs(lt - gt)/n > config.the["cliffs"]


def diffs(nums1, nums2):
  def f(k, nums):
    return cliffDelta(nums["has"], nums2[k]["has"]), nums["txt"]
  return kap(nums1, f)


def cells(s):
  t = {}
  for s1 in re.findall("([^,]+)", s):
    t[len(t)] = coerce(s1)
  return t


def lines(sFilename, fun):
  with open(sFilename, "r") as src:
    rl = src.readlines()
  for s in rl:
    fun(s)


def csv(sFilename, fun):
  lines(sFilename, lambda line: fun(cells(line)))


def push(t, x):
  t[len(t)] = x
  return x


def at(x):
  return lambda t: t[x]


def lt(x):
  return lambda a,b: a[x] < b[x]


def gt(x):
  return lambda a,b: a[x] > b[x]


def ANY(t):
  return t[rint(hi=len(t) - 1)]


def many(t, n):
  u = {}
  for i in range(0, n):
    push(u, ANY(t))
  return u


def per(t, p=0.5):
  p = math.floor(((p) * len(t)) + 0.5)
  return t[max(1, min(len(t), p))]


def settings(s):
  # Parses the help to get possible the command line arguements
  t={}
  res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
  for k,v in res:
    t[k] = coerce(v)
  return t


def cli(options):
  # Parses the settings parse to put into python understandable form
  for k,v in options.items():
    v = str(v)
    for n, x in enumerate(sys.argv):
      if (x == ("-" + k[0:1])) or (x == ("--" + k)):
        more = False
        try: 
          sys.argv[n+1]
          v = sys.argv[n+1]
          break
        except:
          more = False
        v = v == "False" and True or v == "True" and False or more
    options[k] = coerce(v)
  return options