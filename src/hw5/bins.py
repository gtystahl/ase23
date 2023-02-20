# <!-- vim: set syntax=lua ts=2 sw=2 et : -->
#  This code suppprts entropy-merge discretization. This is an bottom-up entropy-based supervised clustering algorithm
#  that divided numerics into (say) 16 bins, then recursively merges adjacent bins in the splits are less informative than the combination.
#  At its start, this code uses recursive Fastmap to find a few `best` examples, then a sample of the `rest`. `bins.lua`
#  then prunes bins that have similar distributions in `best` and `rest

# This is the main file of hw5. All tests are run here and all the meat is created in the other files

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
    print("\n🔆 %s\n" % str({"pass": passes, "fail": fails, "success": 100*passes/(passes+fails)}))
    exit(fails)

egs = {}
def eg(key,string,fun):
  # This is the base function for creating tests which will be run in main
  global egs
  egs[key]=fun

  # It also adds a way to call that test function into the help
  config.Help = config.Help + ("  -g  %s\t%s\n" % (key,string))

eg("the", "show settings", lambda: oo(config.the))

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

# TODO Start here. Cliffs says its false for acc when it should be true. Need to check either that specifically or each of the "close" values I have ignored up to this point
eg("sway","optimizing", checkSway)

eg("bins", "find deltas between best and rest", checkBins)

main(config.the, config.Help, egs)
