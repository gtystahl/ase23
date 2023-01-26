from num import NUM
from sym import SYM
from dataClass import DATA
from helpers import *
import config

# This is the file that holds the functions for all of the tests

def oo(t):
  # This is the regular settings testing function to make sure things are working
  print(t)

def checkSyms():
  # Checks to make sure the syms are working
  sym = SYM()
  for x in ["a","a","a","a","b","b","c"]:
    sym.add(x)
  return "a" == sym.mid() and 1.379 == rnd(sym.div())

def checkNums():
  # Checks to make sure the nums are working
  num = NUM()
  for x in [1,1,1,1,2,2,3]:
    num.add(x)
  return 11/7 == num.mid() and 0.787 == rnd(num.div())

def readCSV():
  # Reads data from a csv and checks to see if all rows and columns are accounted for
  global n
  n = 0
  def f(t):
    global n
    n += len(t)
  csv(config.the["file"], f)
  return n == 8 * 399

def readDataCSV():
  # Reads data from a csv and puts it into a DATA format for analysis.
  data = DATA(config.the["file"])

  # I changed the 1 to a zero because of python indexing starting at 0
  return len(data.rows) == 398 and \
    data.cols.y[0].w == -1 and \
    data.cols.x[0].at == 0 and \
    len(data.cols.x) == 4

def checkStats():
  # Reads data like readDataCSV, but this time evaluates the mid and div of each non-ignored column
  data = DATA(config.the["file"])
  for k, cols in enumerate([data.cols.y, data.cols.x]):
    if k == 0:
      k = "y"
    else:
      k = "x"
    print(k, "\tmid", "\t" + str(data.stats("mid", cols, 2)))
    print("", "\tdiv", "\t" + str(data.stats("div", cols, 2)))