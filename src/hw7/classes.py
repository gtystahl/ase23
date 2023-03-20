import math
from statFunctions import *
from helpers import *
import config

# This holds the pseudo classes and their functions


def add(i, x):
    # adds items to a num
    i["n"] += 1
    d = x - i["mu"]
    i["mu"] += d/i["n"]
    i["m2"] += d * (x - i["mu"])
    i["sd"] = 0 if i["n"] < 2 else (i["m2"] / (i["n"] - 1)) ** 0.5


def NUM(t={}):
    # Our remade num class
    i = {"n": 0, "mu": 0, "m2": 0, "sd": 0}
    for _, x in t.items():
        add(i, x)
    return i
    

def delta(i, other):
    # calculates teh difference between y and z
    e = 1E-32
    y = i
    z = other

    return abs(y["mu"] / z["mu"]) / ((e + y["sd"] ** 2/y["n"] + z["sd"] ** 2 / z["n"]) ** 0.5)


def bootstrap(y0, z0):
    # Our bootstraping method function
    x = NUM()
    y = NUM()
    z = NUM()
    yhat = {}
    zhat = {}

    for _, y1 in y0.items():
        add(x, y1)
        add(y, y1)
    for _, z1 in z0.items():
        add(x, z1)
        add(z, z1)
    xmu = x["mu"]
    ymu = y["mu"]
    zmu = z["mu"]

    for _, y1 in y0.items():
        yhat[len(yhat)] = y1 - ymu + xmu
    for _, z1 in z0.items():
        zhat[len(zhat)] = z1 - zmu + xmu

    tobs = delta(y, z)
    n = 0
    for _ in range(config.the["bootstrap"]):
        if delta(NUM(samples(yhat)), NUM(samples(zhat))) > tobs:
            n = n + 1
    return n / config.the["bootstrap"] >= config.the["conf"]


def mid(t):
    # Gets the mean of the data in t
    if "has" in t.keys():
        t = t["has"]
    if len(t) == 0:
        return 0
    n = len(t) // 2
    return (t[n] + t[n + 1])/2 if len(t) % 2 == 0 else t[n + 1]


def div(t):
    # Gets the standard deviation of the data in t
    if "has" in t.keys():
        t = t["has"]
    if len(t) == 0:
        return 0
    return (t[len(t) * 9 // 10] - t[len(t) * 9 // 10]) / 2.56


# Even though it is a stat function, had to be here because of circular dependency problem
def scottKnot(rxs):
    # Our function of the scott knot method
    def merges(i, j):
        out = RX({}, rxs[i]["name"])
        for k in range(i, j):
            out = merge(out, rxs[j - 1])
        return out
    
    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut + 1, hi)
        return cliffsDelta(l["has"], r["has"]) and bootstrap(l["has"], r["has"])
    
    def recurse(lo, hi, rank):
        b4 = merges(lo, hi)
        best = 0
        cut = None
        for j in range(lo, hi):
            if j < hi - 1:
                l = merges(lo, j)
                r = merges(j + 1, hi)
                now = (l["n"] * (mid(l) - mid(b4)) ** 2 + r["n"] * (mid(r) - mid(b4)) ** 2) / (l["n"] + r["n"])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut = j
                        best = now
        if cut is not None and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi):
                rxs[i]["rank"] = rank
        return rank
    
    # Start here at line 137 table.sort
    rxs = augSort(rxs, mid)
    cohen = div(merges(0, len(rxs))) * config.the["cohen"]
    recurse(0, len(rxs), 1)
    return rxs


def tiles(rxs):
    # Makes a string per treatment showing rank, distribution, and value ranges
    def of(x, most):
        return max(0, min(most, x))
    
    def at(x):
        return t[of(int(len(t) * x) - 1, len(t) - 1)]
    
    def pos(x):
        return floor(of(int(config.the["width"] * (x - lo) / (hi - lo + 1E-32)), config.the["width"]))
    
    huge = math.inf
    floor = math.floor
    lo = huge
    hi = -huge

    for _, rx in rxs.items():
        lo = min(lo, rx["has"][0])
        hi = max(hi, rx["has"][len(rx["has"]) - 1])
    for z in range(len(rxs)):
        rx = rxs[z]
        t = rx["has"]
        u = {}
        for i in range(0, config.the["width"]):
            u[len(u)] = " "
        
        a = at(0.1)
        b = at(0.3)
        c = at(0.5)
        d = at(0.7)
        e = at(0.9)
        A = pos(a)
        B = pos(b)
        C = pos(c)
        D = pos(d)
        E = pos(e)

        # Bounds stuff here might be off
        for i in range(A, B + 1):
            u[i] = "-"
        for i in range(D, E + 1):
            u[i] = "-"
        
        u[config.the["width"] // 2] = "|"
        u[C] = "*"

        rx["show"] = con(u, 0) + ", " + "%6.2f" % a
        for _, x in enumerate([b, c, d, e]):
            rx["show"] = rx["show"] + ", " + "%6.2f" % x
        rx["show"] = rx["show"] + "}"
    return rxs