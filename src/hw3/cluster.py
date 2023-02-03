#             ___                        __                     
#            /\_ \                      /\ \__                  
#      ___   \//\ \     __  __    ____  \ \ ,_\     __    _ __  
#     /'___\   \ \ \   /\ \/\ \  /',__\  \ \ \/   /'__`\ /\`'__\
#    /\ \__/    \_\ \_ \ \ \_\ \/\__, `\  \ \ \_ /\  __/ \ \ \/ 
#    \ \____\   /\____\ \ \____/\/\____/   \ \__\\ \____\ \ \_\ 
#     \/____/   \/____/  \/___/  \/___/     \/__/ \/____/  \/_/ 

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

eg("data", "read DATA csv", readDataCSV)

eg("clone", "duplicate structure", checkClone)

eg("around", "sorting nearest neighbors", checkAround)

eg("half", "1-level bi-clustering", checkHalf)

eg("cluster", "N-level bi-clustering", checkCluster)

eg("optimize", "semi-supervised optimization", checkOptimize)

eg("stats", "stats from DATA", checkStats)

main(config.the, config.Help, egs)
