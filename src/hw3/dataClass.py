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
        data = DATA([self.cols.names])
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
        
    def better(self, row1, row2):
        s1 = 0
        s2 = 0
        ys = self.cols.y

        for _,col in enumerate(ys):
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y) / len(ys))
            s2 = s2 - math.exp(col.w * (y-x) / len(ys))
        return (s1 / len(ys)) < (s2 / len(ys))
    
    def dist(self, row1, row2, cols=None):
        n = 0
        d = 0
        if not cols:
            cols = self.cols.x

        for _,col in enumerate(cols):
            n = n + 1
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ** config.the["p"]
        return (d/n) ** (1 / config.the["p"])
    
    def around(self, row1, rows=None, cols=None):
        global row, dist
        def f(row2):
            global row, dist
            row = row2
            dist = self.dist(row1, row2, cols)
            return [row, dist]
        if not rows:
            rows = self.rows
        return sort(MAP(rows, f), sf) # Might need to change
    
    def half(self, rows=None, cols=None, above=None):
        def project(row):
            x2, y = cosine(dist(row, A), dist(row, B), c)
            return [row, x2]
        
        def dist(row1, row2):
            return self.dist(row1, row2, cols)
        
        if not rows:
            rows = self.rows
        
        some = many(rows, config.the["Sample"])
        if above:
            A = above
        else:
            A = ANY(some)
        
        # Python keeps it as a float so convert to int
        index = int(config.the["Far"] * len(rows) // 1)
        # [0] because of sf return
        B = self.around(A, some)[index][0]

        c = dist(A, B)

        left = []
        right = []

        for n,tmp in enumerate(sort(MAP(rows, project), sf)):
            if n <= len(rows) // 2:
                # [0] for row
                left.append(tmp[0])
                mid = tmp[0]
            else:
                # [0] for row
                right.append(tmp[0])
        return left, right, A, B, mid, c
        

    def cluster(self, rows=None, min=None, cols=None, above=None):
        if not rows:
            rows = self.rows
        
        if not min:
            min = len(rows) ** config.the["min"]
        
        if not cols:
            cols = self.cols.x

        node = [self.clone(rows), None, None, None, None, None]

        if len(rows) > 2 * min: # There is no way this node stuff works
            left, right, node[1], node[2], node[3], _ = self.half(rows, cols, above)

            node[4] = self.cluster(left, min, cols, node[1])
            node[5] = self.cluster(right, min, cols, node[2])
        return node
    
    def sway(self, rows=None, min=None, cols=None, above=None):
        if not rows:
            rows = self.rows
        
        if not min:
            min = len(rows) ** config.the["min"]
        
        if not cols:
            cols = self.cols.x

        node = [self.clone(rows), None, None, None, None, None]

        if len(rows) > 2 * min: # There is no way this node stuff works
            left, right, node[1], node[2], node[3], _ = self.half(rows, cols, above)

            if self.better(node[2], node[1]):
                left, right, node[1], node[2] = right, left, node[2], node[1]
            node[4] = self.sway(left, min, cols, node[1])
        return node
    
