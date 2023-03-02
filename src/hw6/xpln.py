# This code supports multi-goal semi-supervised explanation.  Here,  optimization 
# is treated as a kind of data mining; i.e.  we recursively bi-cluster (using the 
# distance to two remote points), all the while pruning the  "worst" half of the 
# data (as measured by a multi-goal domination predicate).
# During this, we  only label one or two points per cluster. Afterwards, 
# the rules we generate to explain the better rows is generated from the delta between best cluster and the rest.</p>

# This is the main file of hw6. All tests are run here and all the meat is created in the other files

# I kept the main running the same for simplicty of automation on my side
  
from tests import *
import config

def main(options: dict, HELP, funs):
  # This function runs the tests specified by the user on the run (defined in -h or --help)
    saved, fails, passes = {}, 0, 0
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
            passes += 1
            print("✅ pass:","\t" + what)
    print("\n🔆 %s\n" % str({"pass": passes, "fail": fails, "success": 100*passes/(passes+fails) if passes + fails != 0 else 0}))
    exit(fails)

egs = {}
def eg(key,string,fun):
  # This is the base function for creating tests which will be run in main
  global egs
  egs[key]=fun

  # It also adds a way to call that test function into the help
  config.Help = config.Help + ("  -g  %s\t%s\n" % (key,string))

eg("Is", "show options", lambda: oo(config.the))

eg("rand", "demo random number generation", checkRand)

eg("some","demo of reservoir sampling", checkSome)

eg("nums","demo of NUM", checkNums)

eg("syms","demo SYMS", checkSyms)

eg("csv","reading csv files", checkCsv)

eg("data", "showing data sets", checkData)

eg("clone","replicate structure of a DATA", checkClone)

eg("cliffs","stats tests", checkCliffs)

eg("dist","distance test", checkDist)

eg("half","divide data in halg", checkHalf)
 
eg("tree","make snd show tree of clusters", checkTree)

eg("sway","optimizing", checkSway)

eg("bins", "find deltas between best and rest", checkBins)

eg("xpln", "explore explanation sets", checkXPLN)

main(config.the, config.Help, egs)
