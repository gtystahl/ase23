"""
from num import NUM
from sym import SYM
from row import ROW

def pretty(object):
  # Pretty prints the objects given to it (NUM, SYM, ROW, and grid)
  if type(object) == NUM:
    print("{:a NUM :at %d :hi %d :lo %d :m2 %.03f :mu %.03f :n %d :txt %s :w %d}" % (object.at, object.hi, object.lo, object.m2, object.mu, object.n, object.txt, object.w))
  elif type(object) == SYM:
    print("{:a SYM :at %d :has %s :most %d :n %d :txt %s}" % (object.at, str(object.has), object.most, object.n, object.txt))
  elif type(object) == ROW:
    cells = "{"
    for i in range(len(object.cells)):
      cells += str(object.cells[i]) + " "
    cells += "}"
    print("{:a ROW :cells %s}" % cells)
  elif type(object) == dict: # Print out huge grid
    print("{", end="")
    for i in range(len(object)):
      print(object[i], end=" ")
    print("}")
  else:
    print("Item not accounted for")
"""

def pretty(object):
  print(object)