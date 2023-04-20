# use grid search as a comparison here
import random
import time
import csv
import os
from scikittests import *
import copy

class GridSearch():
    def __init__(self):
        self.results = []
        self.latestBest = []
    
    def optProblem(self, par1, par2):
        # For simulating complicated execution
        time.sleep(1)
        # Breaks down to optimization of the file
        return (par1) + (-par2)
    
    def findBest(self, X, size=1):
        best = []
        print("Going through the parameters")
        for i in range(len(X)):
            print("Current: %d" % i)
            group = X[i]
            c1 = group[0]
            c2 = group[1]
            res = self.optProblem(c1, c2)
            self.results.append([res, group])
        
        def sf(l):
            return -l[0]
        best = copy.deepcopy(self.results)
        best.sort(key=sf)
        best = best[:size]
        self.latestBest = best
        return best


def generateSpace():
    items = {}
    while len(items) < 100:
        val1 = random.randint(1, 100)
        val2 = random.randint(1, 100)
        pair = [val1, val2]
        hsh = str(val1) + "$" + str(val2)
        if hsh not in items.keys():
            items[hsh] = pair
    nitems = []
    for k, v in items.items():
        nitems.append(v)
    return nitems


def hpoRunner():
    p = "./hpo/"
    if not os.path.exists(p):
        os.mkdir(p)
    os.chdir(p)
    vals = generateSpace()
    with open("curr.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(["Par1+", "Par2-"])
        w.writerows(vals)

    topCluster, topExplain = scitest(verbose=True)

    val = np.genfromtxt(fname=config.currFile, delimiter=",", dtype=float, skip_header=1, missing_values="?", filling_values=0)
    gs = GridSearch()
    print(gs.findBest(val, 10))


if __name__ == "__main__":
    hpoRunner()

