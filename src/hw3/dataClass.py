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
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ^ config.the["p"]
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
    
    def half(self, rows, cols, above):
        def project(row):
            return [row, cosine(dist(row, A), dist(row, B), c)]
        
        def dist(row1, row2):
            return self.dist(row1, row2, cols)
        
        if not rows:
            rows = self.rows
        
        some = many(rows, config.the["Sample"])
        if above:
            A = above
        else:
            A = ANY(some)

        B = self.around(A, some)[config.the["Far"] * len(rows) // 1].row

        c = dist(A, B)

        left = []
        right = []

        for n,tmp in enumerate(sort(MAP(rows, project), sf)):
            if n <= len(rows) // 2:
                left.append(tmp.row)
                mid = tmp.row
            else:
                right.append(tmp.row)
            return left, right, A, B, mid, c
        

    def cluster(self, rows, min, cols, above):
        if not rows:
            rows = self.rows
        
        if not min:
            min = len(rows) ** config.the["min"]
        
        if not cols:
            cols = self.cols.x

        node = [self.clone(rows)]

        if len(rows) > 2 * min: # There is no way this node stuff works
            left, right, node.A, node.B, node.mid = self.half(rows, cols, above)

            node.left = self.cluster(left, min, cols, node.A)
            node.right = self.cluster(right, min, cols, node.B)
        return node
    
    def sway(self, rows, min, cols, above):
        if not rows:
            rows = self.rows
        
        if not min:
            min = len(rows) ** config.the["min"]
        
        if not cols:
            cols = self.cols.x

        node = [self.clone(rows)]

        if len(rows) > 2 * min: # There is no way this node stuff works
            left, right, node.A, node.B, node.mid = self.half(rows, cols, above)
            if self.better(node.B, node.A):
                left, right, node.A, node.B = right, left, node.B, node.A
            node.left = self.sway(left, min, cols, node.A)
        return node
    
