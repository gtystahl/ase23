import math

# This file holds the SYM class

class SYM():
  def __init__(self, at=0, txt=""):
    self.at = at
    self.txt = txt
    self.n = 0
    self.has = {}
    self.most = 0
    self.mode = None

  def add(self, x):
    # Adds another sym value to itself
    if x != "?":
      self.n = self.n + 1
      if x in self.has.keys():
        self.has[x] += 1
      else:
        self.has[x] = 1
      if self.has[x] > self.most:
        self.most = self.has[x]
        self.mode = x

  def mid(self, x=0):
    # Returns the mode of the sym
    return self.mode

  def div(self, x=0):
    # Returns the entropy of the sym
    def fun(p):
      return p * math.log(p, 2)

    e = 0
    for _,n in self.has.items():
      e = e + fun(n / self.n)

    return -e

  def rnd(self, x, n=0):
    # Returns x because syms cannot be rounded
    return x
  
  def dist(self, s1, s2):
    # Returns the distance between two syms
    # Since you cannot calculate it, it returns either a 1 if they are the same or 0 if they are not
    if s1 == "?" or s2 == "?":
      return 1
    
    if s1 == s2:
      return 0
    else:
      return 1