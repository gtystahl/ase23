# NOTE Need to remove the tests I dont use then done editing this file
  
from tests import *
from scikittests import *
import config
from ablation import *
from hpo import *
from february import *

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

# NOTE DOES NOT WORK FOR -all unless you comment everything out
# Runs the current result file test (sway1 or sway2)
eg("autorun", "runs all of the experiements and saves the resutls", autorun)

# Prints the results of the current result file
eg("results", "interprets the results saved by the tests above", getResults)

# Prints both results file
eg("bothResults", "gets both results for comparison", getBothResults)

# Prints the baseline values since I didn't at first
eg("baselines", "gets the info for the baselines", getBenchmarks)

# Runs the ablation study
eg("ablation", "Runs the abltion runner to get the results to compare", ablationRunner)

# Runs the hpo study
eg("hpo", "Runs the hpo runner", hpoRunner)

# Runs the budget study
eg("budget", "tests more budget make the numbers better", budgetTest)

# Runs the february study
eg("feb", "Runs the february runner", febRunner)

main(config.the, config.Help, egs)