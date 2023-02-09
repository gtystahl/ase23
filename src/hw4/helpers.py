import math
import sys
import re
import config
import os
import copy
from pathlib import Path


# This holds all of the supporting functions that are used by some of the other files
def dofile(fname):
  with open(fname, "r") as file:
    rl = file.readlines()

  bigLine = ""
  for line in rl[1:]:
    bigLine += line.rstrip()

  bigLine = bigLine.replace("'", "")
  
  # Go until you find the first "{"
  top = None
  back = None
  active = None
  index = 0
  val = ""
  for i in range(len(bigLine)):
    curr_char = bigLine[i]
    if bigLine[i] == "{":
      if top is None:
        top = {}
        active = top
        active["INDEX"] = 0
        active["BACK"] = back
        name = ""
      else:
        index = active["INDEX"]
        back = active
        active = {}
        active["INDEX"] = 0
        active["BACK"] = back
        name = ""
        named = False

        for a in range(i-1, -1, -1):
          if named == False and bigLine[a] != "=":
            name = index
            index += 1
            break
          elif named == False:
            named = True
            continue

          if bigLine[a] != "," and bigLine[a] != " ":
            name = bigLine[a] + name
          else:
            break
      active["NAME"] = name
      val = ""
    elif bigLine[i] == "}":
      if val != "":
        try:
          val = int(val)
        except:
          pass
        active[active["INDEX"]] = val
        val = ""
      active["INDEX"] += 1
      if back is not None:
        back[active["NAME"]] = active
        active = back
        back = active["BACK"]
      val = ""
    elif bigLine[i] == ",":
      if val != "":
        try:
          val = int(val)
        except:
          pass
        active[active["INDEX"]] = val
        val = ""
      active["INDEX"] += 1
    elif bigLine[i] == " ":
      pass
    else:
      val += bigLine[i]

  # Set current dict to be active dict
  # Go until you find "}"
  # If you find "{" first, add smaller dict noted by name = {} to dict (empty to start)
  # Then go and look into the new set found
  #
  # All dicts at first will contain strings, then parse the strings for , to get the elements
  # The keys to the dict are numbers rather than names as above 
  
  def rec(d):
    if "INDEX" in d.keys():
      d.pop("INDEX")
      d.pop("BACK")
      d.pop("NAME")
    
    for _,value in d.items():
      if type(value) == dict:
        rec(value)
    
    return d

  top = rec(top)
  
  return top

def sf(s):
  # Returns the distance value of the set passed to it
  res = s["dist"]
  return res

def sfX(s):
  # Returns the distance value of the set passed to it
  res = s["x"]
  return res

def last(d):
  return d[len(d) - 1]

def insert(d, element):
  nd = {}
  for i in range(1, len(d) + 1):
    nd[i] = d[i - 1]
  nd[0] = element
  return nd

def transpose(t):
  u = {}
  for i in range(0, len(t[0])):
    u[i] = {}
    for j in range(0, len(t)):
      u[i][j] = t[j][i]
  return u

def show(node, what=None, cols=None, nPlaces=None, lvl=None):
  # This pretty prints the results of the clustering to the screen.
  if node:
      if not lvl:
          lvl = 0
      for i in range(lvl):
          print("|.. ", end="")
      # print(str(len(node["data"].rows)) + " ")
      if (not node["left"]):
        # print(node["data"].stats("mid", node["data"].cols.y, nPlaces))
        print(last(last(node["data"].rows).cells))
      else:
        # print("", end="")
        print("%.f" % rnd(100 * node["c"]))
      show(node["left"], what, cols, nPlaces, lvl+1)
      show(node["right"], what, cols, nPlaces, lvl+1)

def cosine(a, b, c):
  # This is our version of the cosine equation used to find distance
  x1 = ((a ** 2) + (c ** 2) - (b ** 2))/ (2 * c)
  x2 = max(0, min(1, x1))
  y = ((a ** 2) - x2 ** 2) ** .5
  return x2, y

def ANY(t):
  # This gets any one of the elements of t randomly

  # Need a -1 to account for the offset
  i = rint(hi=len(t) - 1)
  return t[i]

def many(t, n):
  # This gets a lot of random elements of t
  
  u = {}
  for i in range(1, n):
    u[len(u)] = ANY(t)
  return u

def rint(lo=0, hi=1):
  # This gets a random integer between the high and low
  return math.floor(0.5 + rand(lo, hi))

def rand(lo=0, hi=1):
  # Gets a random number between the high and low numbers
  config.Seed = (16807 * config.Seed) % 2147483647
  return lo + (hi - lo) * config.Seed / 2147483647

def rnd(n, nPlaces=0):
  # Returns n rounded to the nPlaces
  mult = 0
  if nPlaces:
    mult = 10 ** nPlaces
  else:
    mult = 10 ** 3

  return math.floor(n * mult + 0.5) / mult

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

def sort(t, fun):
  nt = []
  for i in range(len(t)):
    nt.append(t[i])
  nt.sort(key=fun)

  return nt

def keys(t):
  # Returns a list of sorted table keys
  return sort(kap(t, lambda a, b: a))

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