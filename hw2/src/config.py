# This file holds all of global data needed across all of the other files

global the, Help, Seed

the,Help = {},"""
data.py : an example csv reader script
(c)2023, Greg Tystahl <gttystah@ncsu.edu>, BSD-2 

USAGE:   data.py  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file  name of file         = ../etc/data/auto93.csv
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
"""
    
Seed = 927162211