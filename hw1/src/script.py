#                                            __      
#                            __             /\ \__   
#      ____    ___    _ __  /\_\    _____   \ \ ,_\  
#     /',__\  /'___\ /\`'__\\/\ \  /\ '__`\  \ \ \/  
#    /\__, `\/\ \__/ \ \ \/  \ \ \ \ \ \L\ \  \ \ \_ 
#    \/\____/\ \____\ \ \_\   \ \_\ \ \ ,__/   \ \__\
#     \/___/  \/____/  \/_/    \/_/  \ \ \/     \/__/
#                                     \ \_\          
#                                      \/_/          
from tests import *
import config

the = config.the
Help = config.Help
Seed = config.Seed

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