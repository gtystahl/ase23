from num import NUM
from sym import SYM
import re

class COLS():
    def __init__(self, t:dict):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = {}

        for n, s in enumerate(t):
            col = NUM(n, s) if re.search("^[A-Z]+", s) else SYM(n, s)
            self.all.append(col)
            if not re.search("X$", s):
                if re.search("!$", s):
                    self.klass = col
                self.y.append(col) if re.search("[!+-]$", s) else self.x.append(col)

    def add(self, row):
        for _,t in enumerate([self.x, self.y]):
            for _,col in enumerate(t):
                col.add(row.cells[col.at])