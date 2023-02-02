from num import NUM
from sym import SYM
from helpers import *
import config

def oo(t):
  print(t)

def generator():
  num1 = NUM()
  num2 = NUM()

  config.Seed = config.the["seed"]
  for i in range(1, 10 ** 3):
    num1.add( rand(0, 1) )
  config.Seed = config.the["seed"]
  for i in range(1, 10 ** 3):
    num2.add( rand(0, 1) )

  m1 = rnd(num1.mid(), 10)
  m2 = rnd(num2.mid(), 10)
  return m1 == m2 and .5 == rnd(m1, 1)

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