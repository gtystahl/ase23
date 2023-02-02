#    __             __                
#   /\ \           /\ \__             
#   \_\ \      __  \ \ ,_\     __     
#   /'_` \   /'__`\ \ \ \/   /'__`\   
#  /\ \L\ \ /\ \L\.\_\ \ \_ /\ \L\.\_ 
#  \ \___,_\\ \__/.\_\\ \__\\ \__/.\_\
#   \/__,_ / \/__/\/_/ \/__/ \/__/\/_/    

# This is the main file of hw2. All tests are run here and all the meat is created in the other files
  
from tests import *
import config

def main(options: dict, HELP, funs):
  # This function runs the tests specified by the user on the run (defined in -h or --help)
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
  # This is the base function for creating tests which will be run in main
  global egs
  egs[key]=fun

  # It also adds a way to call that test function into the help
  config.Help = config.Help + ("  -g  %s\t%s\n" % (key,string))

eg("the", "show settings", lambda: oo(config.the))

eg("sym", "check syms", checkSyms)

eg("num", "check nums", checkNums)

eg("csv", "read from csv", readCSV)

eg("data", "read DATA csv", readDataCSV)

eg("stats", "stats from DATA", checkStats)

main(config.the, config.Help, egs)
