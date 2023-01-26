from num import NUM
from sym import SYM
from dataClass import DATA
from helpers import *
import config

def oo(t):
  print(t)

def checkSyms():
  sym = SYM()
  for x in ["a","a","a","a","b","b","c"]:
    sym.add(x)
  return "a" == sym.mid() and 1.379 == rnd(sym.div())

def checkNums():
  num = NUM()
  for x in [1,1,1,1,2,2,3]:
    num.add(x)
  return 11/7 == num.mid() and 0.787 == rnd(num.div())

def readCSV():
  global n
  n = 0
  def f(t):
    global n
    n += len(t)
  csv(config.the["file"], f) # config.the["file"], lambda t: n += len(t)
  # print(n)
  # print(8 * 399)
  return n == 8 * 399

def readDataCSV():
  data = DATA(config.the["file"])
  # print(len(data.rows))
  # print(data.cols.y[0].w)
  # print(data.cols.x[0].at)
  # print(len(data.cols.x))
  return len(data.rows) == 398 and \
    data.cols.y[0].w == -1 and \
    data.cols.x[0].at == 0 and \
    len(data.cols.x) == 4
  # I changed the 1 to a zero because of python indexing starting at 0

def checkStats():
  data = DATA(config.the["file"])
  for k, cols in enumerate([data.cols.y, data.cols.x]):
    if k == 0:
      k = "y"
    else:
      k = "x"
    print(k, "\tmid", "\t" + str(data.stats("mid", cols, 2)))
    print("", "\tdiv", "\t" + str(data.stats("div", cols, 2)))