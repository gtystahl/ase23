from sklearn.cluster import BisectingKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import sklearn.datasets
import numpy as np
import config
from helpers import *
from classes import *
import csv
import os
import pickle


# Not much needs to be changed for all of this.
# 1. I need to change the number of evals to be the n_clusters and change that accordingly.
#     Then just keep the set of items that are "good" and compare that to the sway
# 2. I need to functionaize the random forest seperate from the bisector and have good return results rather than prints.
# 3. I need to modify this to be able to be run multiple times and then have a way to push those results to files or DBs to be able
#     to query them and analyse them later. 
# 4. I need to remake the stats functions for the analysis mentioned above as well as the repgrid code and insert ways to
#     change the code to fit the other tests. 


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


def cleanCsv():
  nrows = []
  diffs = []
  with open(config.the["file"], "r") as f:
    r = csv.reader(f)
    start = True
    pvals = []
    for row in r:
      if start:
        for i in range(len(row)):
          item = row[i].rstrip()
          if item[-1] == "X":
            pvals.append(i)
        start = False
        pvals.reverse()
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
      for val in pvals:
        row.pop(val)
      nrows.append(row)
  
  with open(config.currFile, "w", newline='') as f:
    w = csv.writer(f)
    w.writerows(nrows)


# TODO Need to change the number of evaluations since all that is evaluated is the beginning to find the best group
# TODO Check the normalization because it doesn't have any right now!!
def BisectClusterer(data, val):
    smallest = (len(data["rows"])) ** config.the["min"]
    total = len(data["rows"])
    numClusters = 0
    while total > smallest:
      total /= 2
      numClusters += 1
    
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
      
    goodRows = {}
    for i in range(len(groups)):
      item = groups[i]
      if item == bestVal:
        goodRows[len(goodRows)] = data["rows"][i]
    
    bestData = DATA(data, goodRows)
    top, _ = betters(bestData, config.bestNum)
    top = DATA(data, top)
    # print("scikit clustering with %5s evals" % len(bestData["rows"]), stats(top)[0], stats(top, div)[0])
    return top, groups, bestVal

def RFExplainer(data, val, groups, bestVal):
    # Random forest explainer below
    ys = []
    for i in range(len(groups)):
      item = groups[i]
      if item == bestVal:
        ys.append(1)
      else:
        ys.append(0)
    ys = np.array(ys)

    # clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    clf = RandomForestClassifier()
    clf.fit(X=val, y=ys)
    scores = cross_val_score(clf, val, ys)
    # print(scores.mean())
    importants = clf.feature_importances_
    importants = importants.tolist()
    d = []
    if len(importants) != len(data["cols"]["names"]):
      print("Bad lengths")
      exit(1)
    for i in range(len(importants)):
      d.append([importants[i], i])
    def f(i):
      return i[0]
    d.sort(key=f)
    d.reverse()

    importantColumns = []
    for item in d:
      if item[0] != 0:
        importantColumns.append(data["cols"]["names"][item[1]])
    # print(importantColumns)
    # print("done")
    return importantColumns


def scitest():
  # Need to add 20 runs per, grab the best val, then take the mean of the 20 best
  cleanCsv()
  data = DATA(config.currFile)
  val = np.genfromtxt(fname=config.currFile, delimiter=",", dtype=float, skip_header=1, missing_values="?", filling_values=0)

  bestCluster = {}
  bestExplain = {}
  
  for i in range(20):
    print("Current run: %d" % i)
    top, groups, bestVal = BisectClusterer(data, val)
    res = betters(top, 1)
    bestCluster[len(bestCluster)] = res[0][0]
    features = RFExplainer(data, val, groups, bestVal)
    for ind in range(len(features)):
      feat = features[ind]
      if feat in bestExplain.keys():
        bestExplain[feat] += (len(features) - ind)
      else:
        bestExplain[feat] = len(features) - ind

  bestExplainList = []
  for k, v in bestExplain.items():
    bestExplainList.append([k, v])

  def sf(i):
    return -i[1]
  bestExplainList.sort(key=sf)

  topTenBest = {}
  for i in range(10):
    try:
      item = bestExplainList[i]
      name = item[0].rstrip()
      if not (name[-1] == "-" or name[-1] == "+"):
        topTenBest[len(topTenBest)] = name
    except IndexError:
      break

  bestClusterData = DATA(data, bestCluster)
  print("Median of the best values for the cluster with %5s evals" % len(bestClusterData["rows"]), stats(bestClusterData)[0], stats(bestClusterData, div)[0])
  print("Best features extracted:")
  for i in range(len(topTenBest)):
    print("%d. %s" % (i + 1, topTenBest[i]))

  with open("clusterRes.txt", "wb") as f:
    pickle.dump(bestClusterData["rows"], f)
  
  with open("explainResults.txt", "wb") as f:
    pickle.dump(topTenBest, f)
  

def autorun():
  # Things to gather on the second run:
  # 1. Gather the evaluations for the data
  # 2. Gather the groups made by the random forest, not just the features.
  # 
  
  config.the["file"] = "../../../../etc/data/project-data/auto93.csv"
  if not os.path.exists("./results/"):
    os.mkdir("./results/")
  os.chdir("./results/")
  base = os.getcwd()
  
  files = ["auto2.csv", "auto93.csv", "china.csv", "coc1000.csv", "coc10000.csv", "healthCloseIsses12mths0001-hard.csv", "healthCloseIsses12mths0011-easy.csv", "nasa93dem.csv", "pom.csv", "SSM.csv", "SSN.csv"]
  file = "auto93.csv"
  for f in files:
    config.the["file"] = config.the["file"].replace(file, f)
    file = f
    curr = "./" + f.split(".")[0] + "/"
    if not os.path.exists(curr):
      os.mkdir(curr)
    os.chdir(curr)
    print("The current file being looked at:", config.the["file"])
    # DO STUFF
    scitest()
    os.chdir(base)
  print("Done autorunning")


def getResults():
  os.chdir("./results/")
  base = os.getcwd()
  files = ["auto2.csv", "auto93.csv", "china.csv", "coc1000.csv", "coc10000.csv", "healthCloseIsses12mths0001-hard.csv", "healthCloseIsses12mths0011-easy.csv", "nasa93dem.csv", "pom.csv", "SSM.csv", "SSN.csv"]
  results = []
  for f in files:
    directory = f.split(".")[0]
    result = []
    os.chdir("./" + directory + "/")
    
    data = DATA("curr.csv")
    result.append(data)

    with open("clusterRes.txt", "rb") as f:
      result.append(pickle.load(f))

    with open("explainResults.txt", "rb") as f:
      result.append(pickle.load(f))
    
    os.chdir(base)
    results.append(result)

  for result in results:
    data = result[0]
    resData = DATA(data, result[1])
    print("Median of the best values for the cluster with %5s evals" % len(resData["rows"]), stats(resData)[0], stats(resData, div)[0])
    print("Important Features:")
    for i in range(len(result[2])):
      f = result[2][i]
      print("%d. %s" % (i, f))
    print("----------------")