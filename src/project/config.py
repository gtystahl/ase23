# NOTE Combined and completed
# This file holds all of global data needed across all of the other files

global the, Help, Seed, bestNum, currFile, resultType

the,Help = {},"""  
xpln: multi-goal semi-supervised explanation
(c) 2023 Greg Tystahl <gttystah@ncsu.edu> BSD-2
  
USAGE: python3 xpln.py [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins        initial number of bins            = 16
  -bt --bootstrap   number of resamples               = 512
  -c  --cliffs      cliff's delta threshold           = .147
  -co --conf        unknown                           = 0.05
  -cd --cohen       cohenD constant                   = 0.35
  -C  --cliff       cliffs delta constant             = 0.4
  -d  --d           different is over sd*d            = .35
  -f  --file        data file                         = ../../etc/data/project-data/auto93.csv
  -fm --Fmt         format string                     = empty
  -F  --Far         distance to distant               = .95
  -g  --go          start-up action                   = nothing
  -h  --help        show help                         = false
  -H  --Halves      search space for clustering       = 512
  -m  --min         size of smallest cluster          = .5
  -M  --Max         numbers                           = 512
  -p  --p           dist coefficient                  = 2
  -r  --rest        how many of rest to sample        = 4
  -R  --Reuse       child splits reuse a parent pole  = true
  -s  --seed        random number seed                = 937162211
  -w  --width       the width constant                = 40
"""
    
Seed = 937162211

bestNum = 0

currFile = "curr.csv"

resultType = "./results/"
# resultType = "./swayResults/"