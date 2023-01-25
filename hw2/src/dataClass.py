from helpers import *
from row import ROW
from cols import COLS

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
        if self.cols:
            # print(type(t))
            t = t if "ROW" in str(type(t)) else ROW(t)
            # t = t if t.cells else ROW(t)
            # print(type(t))
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)

    def clone(self, init):
        data = DATA(self.cols.names)
        if init:
            MAP(init, lambda x: data.add(x))
        else:
            MAP({}, lambda x: data.add(x))
        return data

    def stats(self, what, cols, nPlaces):
        # Needs work
        def f(k, col):
            if what:
                # return col.rnd(getmetatable(col)[what](col), nPlaces), col.txt
                return col.rnd(getattr(globals()[col](), what), nPlaces), col.txt
            else:
                return col.rnd(getattr(globals()[col](), what), nPlaces), col.txt
                # return col.rnd(getmetatable(col)["mid"](col), nPlaces), col.txt
        fun = f
        if cols:
            return kap(cols, fun)
        else:
            return kap(self.cols.y, fun)
