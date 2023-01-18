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
dict.__str__

print(the, Help)

# TODO Line 24 with the env stuff

def oo(t):
  print(t)

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
  # s:gsub("\n[%s]+[-][%S]+[%s]+[-][-]([%S]+)[^\n]+= ([%S]+)",function(k,v) t[k]=coerce(v) end)
  res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
  for k,v in res:
    t[k] = coerce(v)
  # res = re.findall("\n[%s]", s)
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
    for k,v in cli(settings(HELP)).items(): # Dont think this is exactly right
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
    # Need the b4 stuff here too
    exit(fails)

egs = {}
def eg(key,string,fun):
  global egs, Help
  egs[key]=fun
  Help = Help + ("  -g  %s\t%s\n" % (key,string))

eg("the", "show settings", lambda: oo(the))

main(the, Help, egs)