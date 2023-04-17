from sklearn.cluster import BisectingKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import sklearn.datasets
import numpy as np
import config
from helpers import *
from classes import *
import csv


def zit(data, row1, row2):
  # Returns which row is better (True for row1, False for row2)
  s1 = 0
  s2 = 0
  ys = data["cols"]["y"]
  for _, col in ys.items():
    x = norm(col, row1[col["at"]])
    y = norm(col, row2[col["at"]])
    s1 = s1 - math.exp(col["w"] * (x - y)/len(ys))
    s2 = s2 - math.exp(col["w"] * (y - x)/len(ys))
  return s1 / len(ys) < s2 / len(ys)


def sortCenters(data, t, n=0):
  # My modified sorting-all algorithm for the clusterer
  if n == 0:
    n = len(t)
  # t = data["rows"]
  best = []
  for i in range(len(t)):
    item = t[i].tolist()
    if len(best) == 0:
      best.append(item)
    else:
      for a in range(len(best)):
        item2 = best[a]
        res = zit(data, item, item2)
        if res == True:
          best.insert(a, item)
          if len(best) > n:
            best.pop()
          break
        elif a == len(best) - 1:
          best.append(item)
  return best


def rounder(t):
  nt = []
  for item in t:
    nt.append(round(item))
  return nt


def same(list1, list2):
  list1 = list1.tolist()
  if len(list1) != len(list2):
    return False
  for i in range(len(list1)):
    if list1[i] != list2[i]:
      return False
    
  return True


# TODO Need to change the number of evaluations since all that is evaluated is the beginning to find the best group
# TODO Check the normalization because it doesn't have any right now!!
def scitest():
    nrows = []
    diffs = []
    with open(config.the["file"], "r") as f:
      r = csv.reader(f)
      start = True
      for row in r:
        if start:
          start = False
        else:
          for i in range(len(row)):
            item = row[i].rstrip()
            # Not sure if this works
            try:
              if item != "?":
                float(item)
            except: 
              if not item in diffs:
                diffs.append(item)
              row[i] = str(diffs.index(item))
        row[-1] = row[-1].rstrip()
        nrows.append(row)
    
    with open(config.currFile, "w", newline='') as f:
      w = csv.writer(f)
      w.writerows(nrows)
              
    data = DATA(config.currFile)
    smallest = (len(data["rows"])) ** config.the["min"]
    total = len(data["rows"])
    numClusters = 0
    while total > smallest:
      total /= 2
      numClusters += 1
    
    val = np.genfromtxt(fname=config.currFile, delimiter=",", dtype=float, skip_header=1, missing_values="?", filling_values=0)
    # bkm = BisectingKMeans(n_clusters=numClusters)
    bkm = BisectingKMeans()
    model = bkm.fit(X=val)
    centers = model.cluster_centers_
    centerDict = {}
    for i in range(len(centers)):
      centerDict[i] = centers[i]
    groups = model.labels_.tolist()
    sortedCenters = sortCenters(data, centers)
    best = sortedCenters[0]
    bestVal = -1
    for k, v in centerDict.items():
      if same(v, best):
        bestVal = k
        break
      
    print(bestVal)

    goodRows = {}
    ys = []
    for i in range(len(groups)):
      item = groups[i]
      if item == bestVal:
        goodRows[len(goodRows)] = data["rows"][i]
        ys.append(1)
      else:
        ys.append(0)
    
    bestData = DATA(data, goodRows)
    # This 12 needs to match the others but with some other small changes it will
    top, _ = betters(bestData, config.bestNum)
    top = DATA(data, top)
    print("scikit clustering with %5s evals" % len(bestData["rows"]), stats(top)[0], stats(top, div)[0])

    # Random forest explainer below
    ys = np.array(ys)

    clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    clf.fit(X=val, y=ys)
    scores = cross_val_score(clf, val, ys)
    print(scores.mean())
    importants = clf.feature_importances_
    d = {}
    for i in importants:
      d[len(d)] = i
    importants.sort()

    importantColumns = []
    for i in importants:
      for k, v in d.items():
        if v == i:
          importantColumns.append(data["cols"]["names"][k])
    print(importantColumns)
    print("done")