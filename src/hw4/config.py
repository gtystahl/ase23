# This file holds all of global data needed across all of the other files

global the, Help, Seed

the,Help = {},"""
grid.py : a rep grid processor
(c)2023, Greg Tystahl <gttystah@ncsu.edu>, BSD-2 

USAGE: grid.py  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../../etc/data/repgrid1.csv
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211

ACTIONS:
"""
    
Seed = 937162211
