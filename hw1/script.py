#                                            __      
#                            __             /\ \__   
#      ____    ___    _ __  /\_\    _____   \ \ ,_\  
#     /',__\  /'___\ /\`'__\\/\ \  /\ '__`\  \ \ \/  
#    /\__, `\/\ \__/ \ \ \/  \ \ \ \ \ \L\ \  \ \ \_ 
#    \/\____/\ \____\ \ \_\   \ \_\ \ \ ,__/   \ \__\
#     \/___/  \/____/  \/_/    \/_/  \ \ \/     \/__/
#                                     \ \_\          
#                                      \/_/          
import re
import sys
import math

the,Help = {},"""
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE:   script.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
"""
# print(the, Help)

class SYM():
  def __init__(self):
    self.n = 0
    self.has = {}
    self.most = 0
    self.mode = None

  def add(self, x):
    if x != "?":
      self.n = self.n + 1
      if x in self.has.keys():
        self.has[x] += 1
      else:
        self.has[x] = 1
      if self.has[x] > self.most:
        self.most = self.has[x]
        self.mode = x

  def mid(self, x=0):
    return self.mode

  def div(self, x=0):
    def fun(p):
      return p * math.log(p, 2)

    e = 0
    for _,n in self.has.items():
      e = e + fun(n / self.n)

    return -e
    
class NUM():
  def __init__(self):
    self.n = 0
    self.mu = 0
    self.m2 = 0
    self.lo = -math.inf
    self.hi = math.inf

  def add(self, n):
    if n != "?":
      self.n += 1
      d = n - self.mu
      self.mu = self.mu + d/self.n
      self.m2 = self.m2 + d*(n - self.mu)
      self.lo = min(n, self.lo)
      self.hi = max(n, self.hi)

  def mid(self, x=0):
    return self.mu

  def div(self, x=0):
    # Ouf
    return (self.m2 < 0 or self.n < 2) and 0 or (self.m2 / (self.n - 1)) ** 0.5

Seed = 927162211
def rint(lo, hi):
  return math.floor(0.5 + rand(lo, hi))

def rand(lo, hi):
  global Seed

  if not lo:
    lo = 0
  
  if not hi:
    hi = 1

  Seed = (16807 * Seed) % 2147483647

  return lo + (hi - lo) * Seed / 2147483647

def rnd(n, nPlaces=0):
  mult = 0
  
  if nPlaces:
    mult = 10 ** nPlaces
  else:
    mult = 10 ** 3

  return math.floor(n * mult + 0.5) / mult
  

def oo(t):
  print(t)

def generator():
  global Seed
  num1 = NUM()
  num2 = NUM()

  Seed = the["seed"]
  for i in range(1, 10 ** 3):
    num1.add( rand(0, 1) )
  Seed = the["seed"]
  for i in range(1, 10 ** 3):
    num2.add( rand(0, 1) )

  m1 = rnd(num1.mid(), 10)
  m2 = rnd(num2.mid(), 10)
  return m1 == m2 and .5 == rnd(m1, 1)

def checkSyms():
  sym = SYM()
  for x in ["a","a","a","a","b","b","c"]:
    sym.add(x)
  # print(sym.mid())
  # print(rnd(sym.div()))
  return "a" == sym.mid() and 1.379 == rnd(sym.div())

def checkNums():
  num = NUM()
  for x in [1,1,1,1,2,2,3]:
    num.add(x)
  return 11/7 == num.mid() and 0.787 == rnd(num.div())

def coerce(s):
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
    # print("Trying int")
    res = int(s)
  except:
    try:
      # print("Trying float")
      res = float(s)
    except:
      res = fun(re.match("^\s*(.+)\s*$", s).string)
  return res

def settings(s):
  t={}
  res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
  for k,v in res:
    t[k] = coerce(v)
  return t

def cli(options):
  for k,v in options.items():
    v = str(v)
    for n, x in enumerate(sys.argv):
      # print(x == ("-" + k[0:1]))
      # print(x == ("--" + k))
      if (x == ("-" + k[0:1])) or (x == ("--" + k)):
        # print("Got inside the if")
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

def main(options: dict, HELP, funs):
    global Seed
    saved, fails = {}, 0
    for k,v in cli(settings(HELP)).items(): 
      options[k] = v
      saved[k] = v
    if options["help"]:
      print(HELP)
    else:
      for what in funs:
        if options["go"] == "all" or what == options["go"]:
          for k,v in saved.items():
            options[k] = v
          Seed = options["seed"]
          if funs[what]() == False:
            fails = fails + 1
            print("❌ fail:",what)
          else:
            print("✅ pass:",what)
    exit(fails)

egs = {}
def eg(key,string,fun):
  global egs, Help
  egs[key]=fun
  Help = Help + ("  -g  %s\t%s\n" % (key,string))

eg("the", "show settings", lambda: oo(the))

eg("rand", "generate, reset, regenerate same", generator)

eg("sym", "check syms", checkSyms)

eg("num", "check nums", checkNums)

main(the, Help, egs)