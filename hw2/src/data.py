#    __             __                
#   /\ \           /\ \__             
#   \_\ \      __  \ \ ,_\     __     
#   /'_` \   /'__`\ \ \ \/   /'__`\   
#  /\ \L\ \ /\ \L\.\_\ \ \_ /\ \L\.\_ 
#  \ \___,_\\ \__/.\_\\ \__\\ \__/.\_\
#   \/__,_ / \/__/\/_/ \/__/ \/__/\/_/    

  
from tests import *
import config

def main(options: dict, HELP, funs):
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
          config.Seed = options["seed"]
          if funs[what]() == False:
            fails = fails + 1
            print("❌ fail:", "\t" + what)
          else:
            print("✅ pass:","\t" + what)
    exit(fails)

egs = {}
def eg(key,string,fun):
  global egs
  egs[key]=fun
  config.Help = config.Help + ("  -g  %s\t%s\n" % (key,string))

eg("the", "show settings", lambda: oo(config.the))

eg("sym", "check syms", checkSyms)

eg("num", "check nums", checkNums)

eg("csv", "read from csv", readCSV)

eg("data", "read DATA csv", readDataCSV)

eg("stats", "stats from DATA", checkStats)

main(config.the, config.Help, egs)