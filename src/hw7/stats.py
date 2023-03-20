# This is the main file of hw7. All tests are run here and all the meat is created in the other files

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

  
# Runs all of the functions in tests.py
eg("ok", "check ok function", ok)

eg("sample", "check sample function", sample)

eg("num", "check num function", num)

eg("gauss", "check gauss function", gauss)

eg("bootmu", "check bootmu function", bootmu)

eg("pre", "check pre function", pre)

eg("five", "check five function", five)

eg("six", "check six function", six)

eg("tiles", "check tiles function", til)

eg("sk", "check sk function", sk)

main(config.the, config.Help, egs)
