# This file holds all of global data needed across all of the other files

global the, Help, Seed

the,Help = {},"""
cluster.py : an example csv reader script
(c)2022, Greg Tystahl <gttystah@ncsu.edu>, BSD-2 

USAGE: cluster.py  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../../etc/data/auto93.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512

ACTIONS:
"""
    
Seed = 927162211
