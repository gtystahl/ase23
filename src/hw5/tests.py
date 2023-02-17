from newClasses import *
from newHelpers import *
from comboFuncs import *
import config

# This is the file that holds the functions for all of the tests


def close(val1, val2):
  # This checks to make sure that the function works within 0.01
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
  m = config.the["Max"]
  config.the["Max"] = 32
  num1 = NUM()
  for i in range(1, 10001):
    add(num1, i)
  oo(has(num1))
  config.the["Max"] = m


def checkNums():
  num1 = NUM()
  num2 = NUM()
  for i in range(1, 10001):
    add(num1, rand())
  for i in range(1, 10001):
    add(num2, rand() ** 2)
  print(1, rnd(mid(num1)), rnd(div(num1)))
  print(2, rnd(mid(num2)), rnd(div(num2)))
  # print(0.5 == rnd(mid(num1)))
  # print(mid(num1) > mid(num2))
  return close(0.5, rnd(mid(num1))) and mid(num1) > mid(num2)


def checkSyms():
  sym = adds(SYM(), {0: "a", 1: "a", 2: "a", 3: "a", 4: "b", 5: "b", 6: "c"})
  print(mid(sym), rnd(div(sym)))
  return close(1.38, rnd(div(sym)))


def checkCsv():
  global n
  n = 0
  def f(t):
    global n
    n = n + len(t)
  csv(config.the["file"], f)
  return n == 3192


def checkData():
  data = DREAD(config.the["file"])
  col = data["cols"]["x"][0]
  print(col["lo"], col["hi"], mid(col), div(col))
  oo(stats(data))


def checkClone():
  data1 = DREAD(config.the["file"])
  data2 = DCLONE(data1, data1["rows"])
  oo(stats(data1))
  oo(stats(data2))


def checkCliffs():
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
    # j = 1.13


def checkDist():
  data = DREAD(config.the["file"])
  num = NUM()
  for _,row in data["rows"].items():
    add(num, dist(data, row, data["rows"][0]))
  oo({"lo": num["lo"], "hi": num["hi"], "mid": rnd(mid(num)), "div": rnd(div(num))})


def checkHalf():
  data = DREAD(config.the["file"])
  left, right, A, B, c = half(data)
  print(len(left), len(right))
  l = DCLONE(data, left)
  r = DCLONE(data, right)
  print("l", stats(l)[0])
  print("r", stats(r)[0])
 

def checkTree():
  showTree(tree(DREAD(config.the["file"])))


def checkSway():
  data = DREAD(config.the["file"])
  best, rest = sway(data)
  print("\nall ", stats(data)) 
  print("    ",   stats(data,div)) 
  print("\nbest", stats(best)) 
  print("    ",   stats(best,div)) 
  print("\nrest", stats(rest)) 
  print("    ",   stats(rest,div)) 
  print("\nall ~= best?", diffs(best["cols"]["y"], data["cols"]["y"]))
  print("best ~= rest?", diffs(best["cols"]["y"], rest["cols"]["y"]))


def checkBins():
  return False