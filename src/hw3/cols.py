from num import NUM
from sym import SYM
import re

# This file holds the COLS class

class COLS():
    def __init__(self, t):
        if type(t) == list:
            nt = {}
            for item in t:
                nt[len(nt)] = item
            t = nt
        self.names = t
        self.all = {}
        self.x = {}
        self.y = {}
        self.klass = None

        for n, s in t.items():
            col = NUM(n, s) if re.search("^[A-Z]+", s) else SYM(n, s)
            self.all[len(self.all)] = col
            if not re.search("X$", s):
                if re.search("!$", s):
                    self.klass = col
                if re.search("[!+-]$", s):
                    self.y[len(self.y)] = col
                else:
                    self.x[len(self.x)] = col

    def add(self, row):
        # Adds the elements of the row to its correct column
        for _,t in enumerate([self.x, self.y]):
            for _,col in t.items():
                col.add(row.cells[col.at])