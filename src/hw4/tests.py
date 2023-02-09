from num import NUM
from sym import SYM
from dataClass import DATA
from helpers import *
from repFuncs import *
from pretty import pretty
import config

# This is the file that holds the functions for all of the tests

def oo(t):
  # This is the regular settings testing function to make sure things are working
  print(t)

def checkCopy():
  t1 = {"a": 1, "b": {"c": 2, "d": 3}}
  t2 = copy.deepcopy(t1)
  t2["b"]["d"] = 10000
  print("b4", t1, "\nafter", t2)
  return True  

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

def checkRepCols():
  # Checks to see if the data was read from the input csv correctly
  t = repCols(dofile(config.the["file"])["cols"])
  MAP(t.cols.all, pretty)
  MAP(t.rows, pretty)
  return True

def checkColsCluster():
  # Checks to see if the data can be clustered properly
  show(repCols(dofile(config.the["file"])["cols"]).cluster())
  return True

def checkRepRows():
  # Checks to see if the transpose works properly
  t = dofile(config.the["file"])
  rows = repRows(t, transpose(t["cols"]))
  MAP(rows.cols.all, pretty)
  MAP(rows.rows, pretty)
  return True

def checkRepCluster(): 
  # Checks to see if the clustering on the rows works properly
  t = dofile(config.the["file"])
  rows = repRows(t, transpose(t["cols"]))
  show(rows.cluster())
  return True

def checkRepPlace():
  # Displays the clustering 
  t = dofile(config.the["file"])
  rows = repRows(t, transpose(t["cols"]))
  rows.cluster()
  repPlace(rows)

def checkRepgrid():
  # Displays all of the checks above
  repgrid(config.the["file"])