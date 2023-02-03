import math
import re
from helpers import rnd

# This file holds the NUM class

class NUM():
  def __init__(self, at=0, txt=""):
    self.at = at
    self.txt = txt
    self.n = 0
    self.mu = 0
    self.m2 = 0
    self.lo = math.inf
    self.hi = -math.inf
    self.w = -1 if re.search("-$", self.txt) else 1

  def add(self, n):
    # Adds another nums value to this one
    if n != "?":
      self.n += 1
      d = n - self.mu
      self.mu = self.mu + d/self.n
      self.m2 = self.m2 + d*(n - self.mu)
      self.lo = min(n, self.lo)
      self.hi = max(n, self.hi)

  def mid(self, x=0):
    # Returns the mean of the num
    return self.mu

  def div(self, x=0):
    # Returns the standard deviation of the num
    return 0 if (self.m2 < 0 or self.n < 2) else (self.m2 / (self.n - 1)) ** 0.5

  def rnd(self, x, n):
    # rounds x to n if x exists
    return x if x == "?" else rnd(x,n)
  
  def norm(self, n):
    top = (n - self.lo)
    bottom = (self.hi - self.lo + 1e-32)
    bottom2 = (self.hi - self.lo + 1E-32)
    res = top / bottom2
    
    return n if n == "?" else res
  
  def dist(self, n1, n2):
    if n1 == "?" and n2 == "?":
      return 1
    
    n1 = self.norm(n1)
    n2 = self.norm(n2)
    if n1 == "?":
      n1 = 1 if n2 < 0.5 else 0
    if n2 == "?":
      n2 = 1 if n1 < 0.5 else 0
    return abs(n1 - n2)