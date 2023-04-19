# use grid search as a comparison here
import random
import time
import csv
import os
from sklearn.model_selection import GridSearchCV

def optProblem(par1, par2):
    time.sleep(1)
    return par1 - par2

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
