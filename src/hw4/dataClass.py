from helpers import *
from row import ROW
from cols import COLS
from num import NUM
from sym import SYM

# Holds the DATA class and methods

class DATA():
    def __init__(self, src):
        self.rows = {}
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
        # TODO REMOVE THIS!!
        # if t == 0:
        #     print("bad")
        if self.cols:
            t = t if "ROW" in str(type(t)) else ROW(t)
            self.rows[len(self.rows)] = t
            self.cols.add(t)
        else:
            self.cols = COLS(t)
            # print(self.cols)

    def clone(self, init):
        # Clones this data into another data object
        data = DATA({0: self.cols.names})
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
    
    def dist(self, row1, row2, cols=None):
        # Gets the distance between row1 and row2 between 0 to 1
        n = 0
        d = 0
        if not cols:
            cols = self.cols.x

        if 0 in cols.keys():
            for i in range(len(cols)):
                col = cols[i]
                n = n + 1
                d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ** config.the["p"]
        else:
            for _,col in cols.items():
                n = n + 1
                d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ** config.the["p"]
        return (d/n) ** (1 / config.the["p"])
    
    def around(self, row1, rows=None, cols=None):
        # Sorts the rows by distance to row1
        def f(row2):
            row = row2
            dist = self.dist(row1, row2, cols)
            return {"row": row, "dist": dist}
        if not rows:
            rows = self.rows
        return sort(MAP(rows, f), sf)
    
    def furthest(self, row1, rows=None, cols=None):
        t = self.around(row1, rows, cols)
        return last(t)
    
    def half(self, rows=None, cols=None, above=None):
        # Divides the data in two using two far points
        def project(row):
            x, y = cosine(dist(row, A), dist(row, B), c)
            # TODO Check these values with debugger. Might be 0
            if row.x is None:
                row.x = x
            if row.y is None:
                row.y = y
            return {"row": row, "x": x, "y": y}
        
        def dist(row1, row2):
            return self.dist(row1, row2, cols)
        
        if not rows:
            rows = self.rows
        
        # some = many(rows, config.the["Sample"])
        if above:
            A = above
        else:
            A = ANY(rows)
        
        # Python keeps it as a float so convert to int
        # TODO Remove potentially
        # index = int(config.the["Far"] * len(rows) // 1)
        B = self.furthest(A, rows)["row"]

        c = dist(A, B)

        left = {}
        right = {}

        for n,tmp in enumerate(sort(MAP(rows, project), sfX)):
            if n < len(rows) // 2:
                # [0] for row
                left[len(left)] = tmp["row"]
                mid = tmp["row"]
            else:
                # [0] for row
                right[len(right)] = tmp["row"]
        return left, right, A, B, mid, c
        

    def cluster(self, rows=None, cols=None, above=None):
        # Returns rows recursivly halved to find data that is similar to each other
        if not rows:
            rows = self.rows
        
        if not cols:
            cols = self.cols.x

        node = {"data": self.clone(rows), 
                "A": None, 
                "B": None,
                "c": None, 
                "mid": None, 
                "left": None, 
                "right": None}

        if len(rows) >= 2 :
            left, right, node["A"], node["B"], node["mid"], node["c"] = self.half(rows, cols, above)

            node["left"] = self.cluster(left, cols, node["A"])
            node["right"] = self.cluster(right, cols, node["B"])
        return node
    