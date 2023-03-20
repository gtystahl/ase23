# This file holds all of global data needed across all of the other files

global the, Help, Seed

the,Help = {},"""  
stats: Statistical Analysis of our Current Model
(c) 2023 Greg Tystahl <gttystah@ncsu.edu> BSD-2
  
USAGE: python3 stats.py [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bootstrap  number of resamples          = 512
  -c  --conf      unknown                      = 0.05
  -C  --cliff     cliffs delta constant        = 0.4
  -d  --cohen     cohenD constant              = 0.35
  -f  --Fmt       format string                = empty
  -w  --width     the width constant           = 40
  -g  --go        start-up action              = nothing
  -h  --help    show help                      = false
  -s  --seed      random number seed           = 937162211
"""
    
Seed = 937162211
