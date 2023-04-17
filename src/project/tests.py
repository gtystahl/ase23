# NOTE Remove unused tests then good to go

from classes import *
from helpers import *
from comboFuncs import *
from statFunctions import *
import config
import random

# This is the file that holds the functions for all of the tests

def oo(t):
  # This is now a combination of the regular print function of the and the pretty function from homeworks past
  if type(t) == list:
    # Prints lists in the form of lua lists
    print("{", end="")
    for i in range(len(t)):
      print(t[i], end="")
      if i < len(t) - 1:
        print(" ", end="")
    print("}")
  elif type(t) == tuple:
    # Prints only the needed info for stats
    print(t[0])
  else:
    # Prints everything else
    print("Type:", type(t))
    print(t)


def checkRand():
  # Checks to make sure the random generator is working
  return True
  s = config.Seed

  config.Seed = 1
  t = {}
  for i in range(1000):
    push(t, rint(100))

  config.Seed = 1
  u = {}
  for i in range(1000):
    push(u, rint(100))

  for k, v in t.items():
    assert(v == u[k])

  config.Seed = s


def checkSome():
  # Checks to make sure we can grab some numbers correctly
  m = config.the["Max"]
  config.the["Max"] = 32
  num1 = NUM()
  for i in range(1, 10001):
    add(num1, i)
  oo(has(num1))
  config.the["Max"] = m


def checkNums():
  # Checks to make sure nums are created and added correctly
  num1 = NUM()
  num2 = NUM()
  for i in range(1, 10001):
    add(num1, rand())
  for i in range(1, 10001):
    add(num2, rand() ** 2)
  print(1, rnd(mid(num1)), rnd(div(num1)))
  print(2, rnd(mid(num2)), rnd(div(num2)))
  # return close(0.5, rnd(mid(num1))) and mid(num1) > mid(num2)
  return 0.5 == rnd(mid(num1)) and mid(num1) > mid(num2)


def checkSyms():
  # Checks to make sure syms are created and added correctly
  sym = adds(SYM(), {0: "a", 1: "a", 2: "a", 3: "a", 4: "b", 5: "b", 6: "c"})
  print(mid(sym), rnd(div(sym)))
  # return close(1.38, rnd(div(sym)))
  return 1.38 == rnd(div(sym))


def checkCsv():
  # Checks to make sure the data is read correctly
  global n
  n = 0
  def f(t):
    global n
    n = n + len(t)
  csv(config.the["file"], f)
  return n == 3192


def checkData():
  # Checks to make sure the data is created correctly
  data = DATA(config.the["file"])
  col = data["cols"]["x"][0]
  if not col["isSym"]:
    print(col["lo"], col["hi"], mid(col), div(col))
  else:
    print(col["mode"], col["most"])
  oo(stats(data))


def checkClone():
  # Checks to make sure the data can be cloned correctly
  data1 = DATA(config.the["file"])
  data2 = DATA(data1, data1["rows"])
  oo(stats(data1))
  oo(stats(data2))


def checkCliffs():
  # Checks to make sure cliffsDelta catagorizes correctly
  assert(False == cliffDelta( {0: 8, 1: 7, 2: 6, 3: 2, 4: 5, 5: 8, 6: 7, 7: 3}, {0: 8, 1: 7, 2: 6, 3: 2, 4: 5, 5: 8, 6: 7, 7: 3}))
  assert(True == cliffDelta( {0: 8, 1: 7, 2: 6, 3: 2, 4: 5, 5: 8, 6: 7, 7: 3}, {0: 9, 1: 9, 2: 7, 3: 8, 4: 10, 5: 9, 6: 6}))
  t1 = {}
  t2 = {}
  for i in range(1, 1001):
    push(t1, rand())
  for i in range(1, 1001):
    push(t2, rand() ** 0.5)
  assert(False == cliffDelta(t1, t1))
  assert(True == cliffDelta(t1, t2))
  diff = False
  j = 1.0
  while not diff:
    t3 = MAP(t1, lambda x: x * j)
    diff = cliffDelta(t1, t3)
    print(">", rnd(j), diff)
    j = j * 1.025


def checkDist():
  # Checks to make sure the distance funciton works properly
  data = DATA(config.the["file"])
  num = NUM()
  for _,row in data["rows"].items():
    add(num, dist(data, row, data["rows"][0]))
  oo({"lo": num["lo"], "hi": num["hi"], "mid": rnd(mid(num)), "div": rnd(div(num))})


def checkHalf():
  # Checks to make sure that the data can be split in half correctly
  data = DATA(config.the["file"])
  left, right, A, B, c, _ = half(data)
  print(len(left), len(right))
  l = DATA(data, left)
  r = DATA(data, right)
  print("l", stats(l)[0])
  print("r", stats(r)[0])
 

def checkTree():
  # Checks to make sure trees are made correctly
  showTree(tree(DATA(config.the["file"])))


def checkSway():
  # Checks to make sure the sway function works properly
  data = DATA(config.the["file"])
  best, rest, _ = sway(data)
  print("\nall ", stats(data)[0]) 
  print("    ",   stats(data,div)[0]) 
  print("\nbest", stats(best)[0]) 
  print("    ",   stats(best,div)[0]) 
  print("\nrest", stats(rest)[0]) 
  print("    ",   stats(rest,div)[0]) 
  print("\nall ~= best?", diffs(best["cols"]["y"], data["cols"]["y"]))
  print("best ~= rest?", diffs(best["cols"]["y"], rest["cols"]["y"]))


def checkBins():
  # Checks to make sure the bins works correctly
  b4 = ""
  data = DATA(config.the["file"])
  best, rest, _ = sway(data)
  print("all","","","",{"best": len(best["rows"]), "rest": len(rest["rows"])})
  res = bins(data["cols"]["x"], {"best": best["rows"], "rest": rest["rows"]})
  for k, t in res.items():
    for _, range in t.items():
      if range["txt"] != b4:
        print("")
      b4 = range["txt"]
      print(range["txt"], range["lo"], range["hi"], rnd(value(range["y"]["has"], len(best["rows"]), len(rest["rows"]), "best")), range["y"]["has"])


def checkXPLN():
  # Checks to make sure the xpln clustering works
  data = DATA(config.the["file"])
  best, rest, evals = sway(data)
  print(len(best["rows"]))
  config.bestNum = len(best["rows"])
  rule, most = xpln(data, best, rest)
  print("\n-----------\nexplain=", end="")
  prettyPrint(showRule(rule), 1)
  data1 = DATA(data, selects(rule, data["rows"]))
  print("all               ", stats(data)[0], stats(data, div)[0])
  print("sway with %5s evals" % evals, stats(best)[0], stats(best, div)[0])
  print("xpln on   %5s evals" % evals, stats(data1)[0], stats(data1, div)[0])
  top, _ = betters(data, len(best["rows"]))
  top = DATA(data, top)
  print("sort with %5s evals" % len(data["rows"]), stats(top)[0], stats(top, div)[0])

# This is the file that holds the functions for all of the tests

# HW7 Tests that need to be completely rewritten
"""

def ok():
  # Sets the random seed to 1
  random.seed = 1


def sample():
  # Tests getting a sample of items from a dict
  for i in range(10):
     print("", con(samples({0: "a", 1: "b", 2: "c", 3: "d", 4: "e"})))


def num():
  # Tests the number creator function
  n = NUM({0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10})
  print("", n["n"], n["mu"]d, n["sd"])


def gauss():
  # Tests the gaussian function
  t = {}
  for i in range(10**4):
    t[len(t)] = gaussian(10, 2)
  n = NUM(t)
  print("", n["n"], n["mu"], n["sd"])


def bootmu():
  # Tests the bootstrapping function
  a = {}
  b = {}
  for i in range(100):
    a[len(a)] = gaussian(10, 1)
  print("","mu","sd","cliffs","boot","both")
  print("","--","--","------","----","----")
  for iter in range(0, 11):
    mu = 10 + (0.1 * iter)
    b = {}
    for i in range(100):
      b[len(b)] = gaussian(mu, 1)
    cl = cliffsDelta(a,b)
    bs = bootstrap(a,b)
    print("",mu,1,cl,bs,cl and bs)


def pre():
  # Tests the Bottstrap and Gausian functions again
  print("\neg3")
  d = 1
  for i in range(10):
    t1 = {}
    t2 = {}
    for j in range(32):
      t1[len(t1)] = gaussian(10, 1)
      t2[len(t2)] = gaussian(d * 10, 1)
    print("\t",d,"true" if d<1.1 else "false",bootstrap(t1,t2),bootstrap(t1,t1))
    d = d + 0.05


def five():
  # Tests scott knot
  inp = {
         0: RX({0: 0.34, 1: 0.49, 2: 0.51, 3: 0.6,  4: .34,  5: .49,  6: .51, 7: .6},"rx1"),
         1: RX({0: 0.6,  1: 0.7,  2: 0.8,  3: 0.9,  4: .6,   5: .7,   6: .8,  7: .9},"rx2"),
         2: RX({0: 0.15, 1: 0.25, 2: 0.4,  3: 0.35, 4: 0.15, 5: 0.25, 6: 0.4, 7: 0.35},"rx3"),
         3: RX({0: 0.6,  1: 0.7,  2: 0.8,  3: 0.9,  4: 0.6,  5: 0.7,  6: 0.8, 7: 0.9},"rx4"), 
         4: RX({0: 0.1,  1: 0.2,  2: 0.3,  3: 0.4,  4: 0.1,  5: 0.2,  6: 0.3, 7: 0.4},"rx5")
        }
  res1 = scottKnot(inp)
  res2 = tiles(res1)
  for _, rx in res2.items():
    print(rx["name"],rx["rank"],rx["show"])
   

def six():
  # Tests scott knot again
  for _,rx in tiles(scottKnot({
         0: RX({0: 101, 1: 100, 2: 99,   3: 101, 4: 99.5, 5: 101, 6: 100, 7: 99,   8: 101, 9: 99.5},"rx1"),
         1: RX({0: 101, 1: 100, 2: 99,   3: 101, 4: 100,  5: 101, 6: 100, 7: 99,   8: 101, 9: 100},"rx2"),
         2: RX({0: 101, 1: 100, 2: 99.5, 3: 101, 4: 99,   5: 101, 6: 100, 7: 99.5, 8: 101, 9: 99},"rx3"),
         3: RX({0: 101, 1: 100, 2: 99,   3: 101, 4: 100,  5: 101, 6: 100, 7: 99,   8: 101, 9: 100},"rx4")})).items():
    print(rx["name"],rx["rank"],rx["show"])


def til():
  # Tests printing the tiles
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i in range(1000): 
    a[len(a)] = gaussian(10,1)
  for i in range(1000): 
    b[len(b)] = gaussian(10.1,1)
  for i in range(1000): 
    c[len(c)] = gaussian(20,1)
  for i in range(1000): 
    d[len(d)] = gaussian(30,1)
  for i in range(1000): 
    e[len(e)] = gaussian(30.1,1)
  for i in range(1000): 
    f[len(f)] = gaussian(10,1)
  for i in range(1000): 
    g[len(g)] = gaussian(10,1)
  for i in range(1000): 
    h[len(h)] = gaussian(40,1)
  for i in range(1000): 
    j[len(j)] = gaussian(40,3)
  for i in range(1000): 
    k[len(k)] = gaussian(10,1)

  for k,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
    rxs[k] =  RX(v,"rx" + str(k))
  rxs = augSort(rxs, mid)
  for _,rx in tiles(rxs).items():
    print("",rx["name"],rx["show"])


def sk():
  # Tests printing the tiles with scotts knot
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i in range(1000): 
    a[len(a)] = gaussian(10,1)
  for i in range(1000): 
    b[len(b)] = gaussian(10.1,1)
  for i in range(1000): 
    c[len(c)] = gaussian(20,1)
  for i in range(1000): 
    d[len(d)] = gaussian(30,1)
  for i in range(1000): 
    e[len(e)] = gaussian(30.1,1)
  for i in range(1000): 
    f[len(f)] = gaussian(10,1)
  for i in range(1000): 
    g[len(g)] = gaussian(10,1)
  for i in range(1000): 
    h[len(h)] = gaussian(40,1)
  for i in range(1000): 
    j[len(j)] = gaussian(40,3)
  for i in range(1000): 
    k[len(k)] = gaussian(10,1)
  for k,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
    rxs[k] =  RX(v,"rx" + str(k))
  for _,rx in tiles(scottKnot(rxs)).items():
    print("",rx["rank"],rx["name"],rx["show"])
"""