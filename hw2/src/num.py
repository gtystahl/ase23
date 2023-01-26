import math
import re
from helpers import rnd

class NUM():
  def __init__(self, at=0, txt=""):
    self.at = at
    self.txt = txt
    self.n = 0
    self.mu = 0
    self.m2 = 0
    self.lo = -math.inf
    self.hi = math.inf
    self.w = -1 if re.search("-$", self.txt) != -1 else 1 # Fixed (Maybe)

  def add(self, n):
    if n != "?":
      self.n += 1
      d = n - self.mu
      self.mu = self.mu + d/self.n
      self.m2 = self.m2 + d*(n - self.mu)
      self.lo = min(n, self.lo)
      self.hi = max(n, self.hi)

  def mid(self, x=0):
    # print("Ran numbers mid")
    return self.mu

  def div(self, x=0):
    # print("Ran numbers div")
    # return (self.m2 < 0 or self.n < 2) and 0 or (self.m2 / (self.n - 1)) ** 0.5 # Fixed (Maybe)
    return 0 if (self.m2 < 0 or self.n < 2) else (self.m2 / (self.n - 1)) ** 0.5

  def rnd(self, x, n):
    return x if x == "?" else rnd(x,n)