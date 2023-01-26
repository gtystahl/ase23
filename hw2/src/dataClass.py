from helpers import *
from row import ROW
from cols import COLS
from num import NUM
from sym import SYM

# Holds the DATA class and methods

class DATA():
    def __init__(self, src):
        self.rows = []
        self.cols = None
        fun = lambda x: self.add(x)
        if "str" in str(type(src)):
            csv(src, fun)
        else:
            if src:
                MAP(src, fun)
            else:
                MAP({}, fun)
    
    def add(self, t):
        # Adds the row t to the columns and rows of this data object
        if self.cols:
            t = t if "ROW" in str(type(t)) else ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)

    def clone(self, init):
        # Clones this data into another data object
        data = DATA(self.cols.names)
        if init:
            MAP(init, lambda x: data.add(x))
        else:
            MAP({}, lambda x: data.add(x))
        return data

    def stats(self, what, cols, nPlaces):
        # This runs the what (method) on the cols to the nPlaces
        def f(k, col):
            # Gets the result of the what method and returns it rounded to nPlaces
            if what:
                res = getattr(col, what)()
                return col.rnd(res, nPlaces), col.txt
            else:
                res = getattr(col, "mid")()
                return col.rnd(res, nPlaces), col.txt
        fun = f
        if cols:
            return kap(cols, fun)
        else:
            return kap(self.cols.y, fun)
