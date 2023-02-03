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

def readDataCSV():
  # Reads data from a csv and puts it into a DATA format for analysis.
  data = DATA(config.the["file"])

  # I changed the 1 to a zero because of python indexing starting at 0
  return len(data.rows) == 398 and \
    data.cols.y[0].w == -1 and \
    data.cols.x[0].at == 0 and \
    len(data.cols.x) == 4

def checkClone():
  # Checks to make sure the data can be cloned to another one if needed
  data1 = DATA(config.the["file"])
  data2 = data1.clone(data1.rows)
  return len(data1.rows) == len(data2.rows) and \
    data1.cols.y[0].w == data2.cols.y[0].w and \
    data1.cols.x[0].at == data2.cols.x[0].at and \
    len(data1.cols.x) == len(data2.cols.x)

def checkAround():
  # Checks to see which rows are arround the one in question
  data = DATA(config.the["file"])
  print(0, 0, data.rows[0].cells)
  for n,t in enumerate(data.around(data.rows[0])):
    if n % 50 == 0:
      print(n, rnd(t["dist"], 2), t["row"].cells)
  return True

def checkHalf():
  # Checks to see if the data can be split in half correctly
  data = DATA(config.the["file"])
  left, right, A, B, mid, c = data.half()
  print(len(left), len(right), len(data.rows))
  print(A.cells, c)
  print(mid.cells)
  print(B.cells)
  return True

def checkCluster():
  # Checks to see the results of the cluster
  data = DATA(config.the["file"])
  show(data.cluster(), "mid", data.cols.y, 1)
  return True

def checkOptimize():
  # Checks to see the results of the sway optimizer function
  data = DATA(config.the["file"])
  show(data.sway(), "mid", data.cols.y, 1)
  return True