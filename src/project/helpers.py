# NOTE There are two defs of merge. Will need to change some based on which merge it needs

import math
import sys
import re
import config
import os
import copy
import re
from pathlib import Path
import random


# My helpers
def lstToDict(lst):
  # Converts lists to dictionaries with numbered keys
  if type(lst) == dict:
    return lst
  d = {}
  for i in range(len(lst)):
    d[i] = lst[i]
  return d


def remSpace(txt):
  res = ""
  start = False
  for c in txt:
    if start or c.isalpha():
      start = True
      res += c
  return res


def close(val1, val2):
  # This checks to make sure that the function works within 0.01 accuracy
  rval1 = round(val1, 2)
  rval2 = round(val2, 2)
  if (rval1 == rval2):
    return True
  elif (rval2 - 0.01 == rval1) or (rval2 + 0.01 == rval1):
    return True
  elif (rval1 - 0.01 == rval2) or (rval1 + 0.01 == rval2):
    return True
  else:
    return False
  

def prettyPrint(obj, t=0):
  if t == 0:
    print(obj)
  elif t == 1:
    # Print the rule in lua form
    i = 0
    print("{", end="")
    for k,v in obj.items():
      i += 1
      print("'%s': {" % k, end="")
      for k2,v2 in v.items():
        if type(v2) == dict:
          print("{", end="")
          for k3, v3 in v2.items():
            if (k3 == 0 or k3 == "0") and len(v2) != 1:
              print(str(v3) + " ", end="")
            else:
              print(str(v3) + "}", end="")
          print("}", end="")
          break
        if (k2 == 0 or k2 == "0") and len(v) != 1:
          print(str(v2) + " ")
        else:
          print(str(v2) + "}", end="")
      if i < len(obj):
        print(", ", end="")
    print("}")
    

# Lua converted functions
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
  # Add an item x to the column

  def sym(t):
    if x in t.keys():
      t[x] = n + t[x]
    else:
      t[x] = n
    if t[x] > col["most"]:
      col["most"] = t[x]
      col["mode"] = x
  
  def num(t):
    col["lo"] = min(x, col["lo"])
    col["hi"] = max(x, col["hi"])
    if len(t) < config.the["Max"]:
      col["ok"] = False
      t[len(t)] = x
    elif rand() < config.the["Max"] / col["n"]:
      col["ok"] = False
      t[rint(1, len(t)) - 1] = x
  
  if x != "?":
    col["n"] = col["n"] + n
    if col["isSym"]:
      sym(col["has"])
    else:
      num(col["has"])


def rint(lo=0, hi=1):
  # This gets a random integer between the high and low
  return math.floor(0.5 + rand(lo, hi))


def rand(lo=0, hi=1):
  # Trial for changing to true random stuff
  return lo + (hi - lo) * random.random()
  # Gets a random number between the high and low numbers
  config.Seed = (16807 * config.Seed) % 2147483647
  return lo + (hi - lo) * config.Seed / 2147483647


def adds(col, t={}):
  # This adds a lot of items to a column
  for _, x in t.items():
    add(col, x)
  return col


def extend(range, n, s):
  # Use a range to cover x and y
  range["lo"] = min(n, range["lo"])
  range["hi"] = max(n, range["hi"])
  add(range["y"], s)


def has(col):
  # Returns the contents of the column (sorted)
  if not col["isSym"] and not col["ok"]:
    col["has"] = lstToDict(sort(col["has"]))
  col["ok"] = True
  return col["has"]


def sort(t, fun=None):
  # Sorts the dictionary and returns a list
  nt = []
  for k in t.keys():
    nt.append(t[k])
  if fun is not None:
    nt.sort(key=fun)
  else:
    nt.sort()

  return nt


def bestOf(data, n):
  # My modified sorting-all algorithm
  t = data["rows"]
  best = []
  for i in range(len(t)):
    item = t[i]
    if len(best) == 0:
      best.append(item)
    else:
      for a in range(len(best)):
        item2 = best[a]
        res = better(data, item, item2)
        if res == True:
          best.insert(a, item)
          if len(best) > n:
            best.pop()
          break
  return lstToDict(best)


def mid(col):
  # Returns a columns central tendency
  return col["mode"] if col["isSym"] else per(has(col), .5)


def div(col):
  # Returns a columns deviation from central tendency
  if col["isSym"]:
    e = 0
    for _, n in col["has"].items():
      e = e - n / col["n"] * math.log(n / col["n"], 2)
    return e
  else:
    return (per(has(col), .9) - per(has(col), .1)) / 2.58
  

def stats(data, fun=mid, cols=None, nPlaces=0):
  # Returns the mid or div of cols
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
  if 0 in t.keys() and False:
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
    mult = 10 ** 2

  return math.floor(n * mult + 0.5) / mult


def norm(num, n):
  # Normalizes n based on num
  # I changed the xs to ns because I am not sure where the x comes from...
  if str(n) == "?":
    return n
  else:
    res = 0
    try:
      res = (n - num["lo"])/((num["hi"] - num["lo"]) + 1/math.inf)
    except:
      if num["lo"] == num["hi"] == 0:
        res = 0
      else:
        res = math.inf
    return res
      
  # return n if str(n) == "?" else (n - num["lo"])/((num["hi"] - num["lo"]) + 1/math.inf)


def value(has, nB=1, nR=1, sGoal=True):
  # Returns to score of a distribution of symbols
  b = 0
  r = 0
  for x, n in has.items():
    if x == sGoal:
      b = b + n
    else:
      r = r + n
  b = b/(nB+1/math.inf)
  r = r/(nR+1/math.inf)
  return b**2 / (b+r)


def dist(data, t1, t2, cols=None):
  # Calculates the distance between t1 and t2 (Normalized)

  def sym(x,y):
    return 0 if x == y else 1
  
  def num(x,y):
    if x == "?":
      x = 1 if y < 0.5 else 1
    if y == "?":
      y = 1 if x < 0.5 else 1
    return abs(x - y)
  
  def dist1(col, x, y):
    if x == "?" and y == "?":
      return 1
    return sym(x, y) if col["isSym"] else num(norm(col, x), norm(col, y))
  
  d = 0
  if cols is None:
    cols = data["cols"]["x"]
  for _, col in cols.items():
    d = d + dist1(col, t1[col["at"]], t2[col["at"]]) ** config.the["p"]
  return (d/len(cols)) ** (1 / config.the["p"])


def better(data, row1, row2):
  # Returns which row is better (True for row1, False for row2)
  s1 = 0
  s2 = 0
  ys = data["cols"]["y"]
  for _, col in ys.items():
    x = norm(col, row1[col["at"]])
    y = norm(col, row2[col["at"]])
    s1 = s1 - math.exp(col["w"] * (x - y)/len(ys))
    s2 = s2 - math.exp(col["w"] * (y - x)/len(ys))
  return s1 / len(ys) < s2 / len(ys)


def betters(data, n):
  # Finds the betters in data with a size of n
  # Modified sort to be O(len(data) * n) which is O(n * c) which is O(n) in terms of algorithm evals
  tmp = bestOf(data, n)
  return tmp, None


def SLICE(t, go=None, stop=None, inc=1):
  # Sliceing function, works like lst[1:]
  if go and go < 0:
    go = len(t) + go
  if stop and stop < 0:
    stop = len(t) + stop
  u = {}
  if go is None:
    go = 0
  if stop is None:
    stop = len(t)
  for j in range(go, stop, inc):
    u[len(u)] = t[j]
  return u


def half(data, rows=None, cols=None, above=None):
  # Splits the data in half based on two distant points
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
  far = tmp[int((len(tmp) - 1) * config.the["Far"])]
  B = far["row"]
  c = far["d"]

  def f2(d):
    return d["x"]
  for n, two in enumerate(sort(MAP(rows, proj), f2)):
    push(left if n < len(rows)/2 else right, two["row"])
  evals = 1 if config.the["Reuse"] and above else 2
  return left, right, A, B, c, evals


def merges(ranges0, nSmall, nFar):
  # Given a sorted list of ranges
  def noGaps(t):
    for j in range(1, len(t)):
      t[j]["lo"] = t[j - 1]["hi"]
    t[0]["lo"] = -math.inf
    t[len(t) - 1]["hi"] = math.inf
    return t
  
  def try2Merge(left, right, j):
    y = merged(left["y"], right["y"], nSmall, nFar)
    if y:
      j = j + 1
      left["hi"] = right["hi"]
      left["y"] = y
    return j, left
  
  ranges1 = {}
  j = 0
  while j < len(ranges0):
    here = ranges0[j]
    if j < len(ranges0) - 1:
      j, here = try2Merge(here, ranges0[j + 1], j)
    j = j + 1
    push(ranges1, here)
  return noGaps(ranges0) if len(ranges0) == len(ranges1) else merges(ranges1, nSmall, nFar)


def merged(col1, col2, nSmall, nFar):
  # If the whole is better than the parts, return the new
  new = merge(col1, col2)
  if nSmall and col1["n"] < nSmall or col2["n"] < nSmall:
    return new
  if nFar and not col1["isSym"] and abs(mid(col1) - mid(col2)) < nFar:
    return new
  if div(new) <= (div(col1)*col1["n"] + div(col2)*col2["n"]) / new["n"]:
    return new
  

def merge(col1, col2):
  # Merge two cols
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


# Simple function that just returns itself
def itself(x): return x


def cliffDelta(ns1, ns2):
  # Non-parametric effect-size test
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
  return abs(lt - gt)/n > config.the["cliffs"]


def diffs(nums1, nums2):
  # given two tables, returns the differences between them
  def f(k, nums):
    return cliffDelta(nums["has"], nums2[k]["has"]), nums["txt"]
  return kap(nums1, f)


def cells(s):
  # Split a string s on commas
  t = {}
  for s1 in re.findall("([^,]+)", s):
    t[len(t)] = coerce(s1)
  return t


def lines(sFilename, fun):
  # Opens a file and sperates the lines of the file and do functions on those lines
  with open(sFilename, "r") as src:
    rl = src.readlines()
  for s in rl:
    fun(s)


def csv(sFilename, fun):
  # Open a csv file and read in the row data
  lines(sFilename, lambda line: fun(cells(line)))


def push(t, x):
  # add an item x to t
  t[len(t)] = x
  return x


def at(x):
  # Return the value of t at x
  return lambda t: t[x]


def lt(x):
  # Return the result of a[x] < b[x]
  return lambda a,b: a[x] < b[x]


def gt(x):
  # Return the result of a[x] > b[x]
  return lambda a,b: a[x] > b[x]


def ANY(t):
  # Get any item of t in range(0 to len - 1)
  return t[rint(lo=len(t), hi=1) - 1]


def many(t, n):
  # Get multiple (n) items from t
  u = {}
  for i in range(0, n):
    push(u, ANY(t))
  return u


def per(t, p=0.5):
  # Return the p ratio item in t
  p = math.floor(((p) * len(t) - 1) + 0.5)
  return t[max(0, min(len(t) - 1, p))]


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

# NOTE HW7 below



def augSort(d, fun=None):
    # My augmented sort function to handle the difference between lua tables and python dicts
    lst = []
    for _, item in d.items():
        lst.append(item)
    if fun is None:
      lst.sort()
    else:
      lst.sort(key=fun)
    nd = {}
    for i in range(len(lst)):
        nd[i] = lst[i]
    return nd


def RX(t,s=""):
    # sorts and returns the data of t in num format
    t = augSort(t)
    return {"name": s, "rank": 0, "n": len(t), "show": "", "has": t}


""""""
def statMerge(rx1, rx2):
    # Merges two "buckets"
    rx3 = RX({}, rx1["name"])
    for _, item in rx1["has"].items():
        rx3["has"][len(rx3["has"])] = item
    for _, item in rx2["has"].items():
        rx3["has"][len(rx3["has"])] = item
    rx3["has"] = augSort(rx3["has"])
    rx3["n"] = len(rx3["has"])
    return rx3


def con(d, std=1):
  # Concatinates items in d
  s = ""
  if std == 1:
    for _, item in d.items():
      s += item
  else:
    for i in range(len(d)):
      s += str(d[i])
  return s

