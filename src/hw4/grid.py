#                             __     
#                     __     /\ \    
#      __      _ __  /\_\    \_\ \   
#    /'_ `\   /\`'__\\/\ \   /'_` \  
#   /\ \L\ \  \ \ \/  \ \ \ /\ \L\ \ 
#   \ \____ \  \ \_\   \ \_\\ \___,_\
#    \/___L\ \  \/_/    \/_/ \/__,_ /
#      /\____/                       
#      \_/__/   

# This is the main file of hw4. All tests are run here and all the meat is created in the other files
  
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
          # Since I added the surveys as tests, this ignores them unless specified to keep them seperate
          if options["go"] == "all" and ("Survey" in what or "Every" == what):
            continue 
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

eg("copy", "check copy", checkCopy)

eg("sym", "check syms", checkSyms)

eg("num", "check nums", checkNums)

eg("repcols","checking repcols", checkRepCols)

eg("synonyms","checking repcols cluster", checkColsCluster)

eg("reprows","checking reprows", checkRepRows)

eg("prototypes","checking reprows cluster", checkRepCluster)

eg("position","where's wally", checkRepPlace)

eg("every","the whole enchilada", checkRepgrid)

# Here are the tests for running the cluster on the surveys (Repgrids)

eg("Survey1", "The repgrid for the first survey", survey1)

eg("Survey2", "The repgrid for the second survey", survey2)

eg("Survey3", "The repgrid for the third survey", survey3)

eg("Every", "This runs all of the serveys", all_surveys)

main(config.the, config.Help, egs)
