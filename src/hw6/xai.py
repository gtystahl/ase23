
# <!-- vim: set syntax=lua ts=2 sw=2 et : -->
# <img style="padding:3px;" src="https://raw.githubusercontent.com/timm/tested/main/etc/img/script.png" align=left width=135>
# <p style="text-align: right;">
#  <a 
#   href="https://zenodo.org/badge/latestdoi/569981645"> <img 
#    src="https://zenodo.org/badge/569981645.svg" alt="DOI"></a><br>
# <img src="https://img.shields.io/badge/task-ai-purple"> <img 
#  src="https://img.shields.io/badge/language-lua5.4-orange"><br><img 
#  src="https://img.shields.io/badge/purpose-teaching-yellow">
# <a href="https://github.com/timm/tested/actions/workflows/tests.yml"><br><img 
#   src="https://github.com/timm/tested/actions/workflows/tests.yml/badge.svg"></a>
#  <br>
# <a href="https://github.com/timm/tested/blob/main/src/xai.lua">download</a> <br>
# <a href="https://github.com/timm/tested/blob/main/etc/data/auto93.csv">example data</a> <br>
# <a href="#license">license</a> <br>
# <a href="https://github.com/timm/tested/issues">issues</a><br clear=all>
#        
# <p style="text-align: left;">
# This code supports multi-goal semi-supervised explanation.  Here,  optimization 
# is treated as a kind of data mining; i.e.  we recursively bi-cluster (using the 
# distance to two remote points), all the while pruning the  "worst" half of the 
# data (as measured by a multi-goal domination predicate).
# During this, we  only label one or two points per cluster. Afterwards, 
# the rules we generate to explain the better rows is generated from the delta between best cluster and the rest.</p>
# For help with code, see comments at the <a href="#about">end of this file</a>.</p>

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

# TODO Start here. Cliffs says its false for acc when it should be true. Need to check either that specifically or each of the "close" values I have ignored up to this point
eg("sway","optimizing", checkSway)

eg("bins", "find deltas between best and rest", checkBins)

eg("xpln", "explore explanation sets", checkXPLN)

main(config.the, config.Help, egs)

# ## <a name=about>About this code</a>
# <p style="text-align: left;">
# The aim here was to achieve as much functionality in as few lines as possible
# (to simplify teaching these ideas as well as any further experimentation).
# All the code for the above functionality comes in at just
# under 300 lines of AI code (plus another 200 lines of  misc support routines). 
# <p style="text-align: left;">
# To read this, code:<br>
# FIRST skim the `help` string (at top);  <br>   
# SECOND browse the structs (see "<a href="#create">Creation</a>");  <br> 
# THIRD read  the <a href="#egs">examples</a> at end.  </p>
# <p style="text-align: left;">
# Note that any of the examples can be run from the command line; 
# e.g. "-g show" runs
# all the actions that start with "show". 
# Also, all the settings in the help string can
# be changed on the command line; e.g. "lua fetchr.lua -s 3" sets the seed to 3.
# Those settings are stored in"the" table, which is generated from
# "help". </p>
# <p style="text-align: left;">
# In the function arguments, the following conventions apply (usually):</p>
#     
# -  Two spaces denote start of optional args
# -  Four spaces denote start of local args. 
# -  n == number
# -  s == string
# -  t == table
# -  is == boolean
# -  x == anything
# -  fun == function
# -  UPPER = class (some factory for making similar things)
# -  lower = instance; e.g. sym is an instance of SYM
# -  xs == a table of "x"; e.g. "ns" is a list of numbers
#     
# <p style="text-align: left;">
# In this language (LUA) vars are global by default unless marked with "local" or 
# defined in function argument lists.
# Also,  there is only one data structure called a "table".
# that can have numeric or symbolic keys.