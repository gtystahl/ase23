# use grid search as a comparison here
import random
import time
import csv
import os
from scikittests import *
import copy


def optProblem(par1, par2):
        # For simulating complicated execution
        time.sleep(1)
        # Breaks down to optimization of the file
        return (par1) + (-par2)


class GridSearch():
    def __init__(self):
        self.results = []
        self.latestBest = []
    
    def findBest(self, X, size=1, problem=optProblem):
        best = []
        print("Going through the parameters")
        for i in range(len(X)):
            print("Current: %d" % i)
            group = X[i]
            c1 = group[0]
            c2 = group[1]
            res = problem(c1, c2)
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
    with open("curr.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Par1+", "Par2-"])
        w.writerows(vals)

    config.the["file"] = "./curr.csv"

    start = time.time()
    topCluster, topExplain = scitest(verbose=True)
    vals = {}
    for keyVal, group in topCluster.items():
        for k, v in group.items():
            if not k in vals.keys():
                vals[k] = v
            else:
                vals[k] += v
    for k, v in vals.items():
        vals[k] = v / len(topCluster)
    inpVals = []
    print("Best average Cluster Vals:")
    for k in vals.keys():
        inpVals.append(round(vals[k]))
        print("[%s]: [%d]" % (k, round(vals[k])))
    bestOutput = optProblem(inpVals[0], inpVals[1])
    end = time.time()
    print("Best output found by cluser: [%d] with a time of %s seconds" % (bestOutput, end - start))

    val = np.genfromtxt(fname=config.currFile, delimiter=",", dtype=float, skip_header=1, missing_values="?", filling_values=0)
    start = time.time()
    gs = GridSearch()
    topTen = gs.findBest(val, len(topCluster))
    vals = [0, 0]
    for result in topTen:
        vals[0] += result[1][0]
        vals[1] += result[1][1]
    for i in range(len(vals)):
        item = vals[i]
        vals[i] = item / len(topCluster)

    gridBest = optProblem(round(vals[0]), round(vals[1]))
    end = time.time()
    print("Best average params found by grid search: Par1+ [%d] and Par2- [%d]" % (vals[0], vals[1]))
    print("Best average result found by grid search: [%d] with a time of %s seconds" % (gridBest, end - start))


if __name__ == "__main__":
    hpoRunner()

