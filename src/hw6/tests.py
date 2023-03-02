from classes import *
from helpers import *
from comboFuncs import *
import config

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
  print(col["lo"], col["hi"], mid(col), div(col))
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
  data = DATA(config.the["file"])
  best, rest, rule, most, evals = xpln(data)
  print("explain=", showRule(rule))
  data1 = DATA(data, selects(rule, data["rows"]))
  print("all               ", stats(data), stats(data, div))
  print("sway with %5s evals" % evals, stats(best), stats(best, div))
  print("xpln on   %5s evals" % evals, stats(data1), stats(data1, div))
  top, _ = betters(data, len(best["rows"]))
  top = DATA(data, top)
  print("sort with %5s evals" % data["rows"], stats(top), stats(top, div))