import math
import sys
import re
import config
import os
from pathlib import Path

# This holds all of the supporting functions that are used by some of the other files
def sf(s):
  # Since I have opted to go for a list structure, 'dist' is 1 while row is 0
  res = s[1]
  return res

def show(node, what, cols, nPlaces, lvl=None):
  if node:
      if not lvl:
          lvl = 0
      for i in range(lvl):
          print("| ", end="")
      print(str(len(node[0].rows)) + " ")
      if (not node[4]) or lvl == 0:
        print(node[0].stats("mid", node[0].cols.y, nPlaces))
      else:
        print("", end="")
      show(node[4], what, cols, nPlaces, lvl+1)
      show(node[5], what, cols, nPlaces, lvl+1)

def cosine(a, b, c):
  x1 = ((a ** 2) + (c ** 2) / (2 * c))
  x2 = max(0, min(1, x1))
  y = ((a ** 2) - x2 ** 2) ** .5
  return x2, y

def ANY(t):
  # Need a -1 to account for the offset
  i = rint(hi=len(t) - 1)
  return t[i]

def many(t, n):
  u = []
  for i in range(1, n):
    u.append(ANY(t))
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
  u = []
  for k, v in enumerate(t):
    v = fun(v)
    u.append(v)
  return u

def kap(t, fun):
  # Like map but requires fun to be fun(k, v) not just v
  u = []
  for k, v in enumerate(t):
    v, k = fun(k, v)
    u.append(v)
  return u

def sort(t:list, fun):
  # Sorts t using the function fun as the key
  t.sort(key=fun)
  return t

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