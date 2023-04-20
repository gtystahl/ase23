from sklearn.cluster import BisectingKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import sklearn.datasets
import numpy as np
import config
from helpers import *
from classes import *
from comboFuncs import *
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
def BisectClusterer(data, val, nClusters=8):
    smallest = (len(data["rows"])) ** config.the["min"]
    total = len(data["rows"])
    numClusters = 0
    while total > smallest:
      total /= 2
      numClusters += 1
    
    # bkm = BisectingKMeans(n_clusters=numClusters)
    bkm = BisectingKMeans(nClusters)
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
    # top, _ = betters(bestData, config.bestNum)
    # top = DATA(data, top)
    # print("scikit clustering with %5s evals" % len(bestData["rows"]), stats(top)[0], stats(top, div)[0])
    # return top, groups, bestVal, len(bestData["rows"]), bestData["rows"]
    return bestData, groups, bestVal, {"Evals": nClusters}, bestData["rows"]

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
    X_train, X_test, y_train, y_test = train_test_split(val, ys)
    clf.fit(X=X_train, y=y_train)
    scores = cross_val_score(clf, X_test, y_test)
    guesses = clf.predict(val)
    guessed_rows = {}
    for i in range(len(data["rows"])):
      if guesses[i] == 1:
        guessed_rows[len(guessed_rows)] = data["rows"][i]
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
    return importantColumns, guessed_rows, {"Score": scores.mean()}


def getAvg(d):
  avgRes = {}
  for k, v in d.items():
    for colName, value in v.items():
      if not colName in avgRes.keys():
        avgRes[colName] = value
      else:
        avgRes[colName] += value
  for k, v in avgRes.items():
    avgRes[k] = v / len(d)
  return avgRes


def scitest(nClusters=8, verbose=False):
  print("Running scitest")
  # Need to add 20 runs per, grab the best val, then take the mean of the 20 best
  cleanCsv()
  data = DATA(config.currFile)
  val = np.genfromtxt(fname=config.currFile, delimiter=",", dtype=float, skip_header=1, missing_values="?", filling_values=0)

  bestCluster = {}
  bestClusterEvals = {}
  bestExplain = {}
  bestExplainValues = {}
  bestExplainScores = {}

  regularClusters = {}
  regularExplains = {}
  
  for i in range(20):
    print("Current run: %d" % i)
    top, groups, bestVal, evals, regular = BisectClusterer(data, val, nClusters)
    regularClusters[len(regularClusters)] = regular
    bestClusterEvals[len(bestClusterEvals)] = evals
    # res = betters(top, 1)
    # bestCluster[len(bestCluster)] = res[0][0]
    bestCluster[len(bestCluster)] = stats(top)[0]
    features, bestExplains, score = RFExplainer(data, val, groups, bestVal)
    bestExplainScores[len(bestExplainScores)] = score
    regularExplains[len(regularExplains)] = bestExplains
    top = DATA(data, bestExplains)
    # res = betters(top, 1)
    # bestExplainValues[len(bestCluster)] = res[0][0]
    bestExplainValues[len(bestExplainValues)] = stats(top)[0]
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

  bestClusterData = getAvg(bestCluster)
  avgEval = getAvg(bestClusterEvals)["Evals"]
  print("Average of the median values for the cluster with %5s evals over 20 runs" % avgEval, bestClusterData)

  bestExplainData = getAvg(bestExplainValues)
  avgScore = getAvg(bestExplainScores)["Score"]
  print("Average of the median values for the explainer with %5s validation score over 20 runs" % avgScore, bestExplainData)

  # avg = 0
  # for k, num in bestClusterEvals.items():
  #   avg += num
  # avg /= len(bestClusterEvals)
  avg_eval = {avgEval}
  avg_score = {avgScore}

  print("Best features extracted:")
  for i in range(len(topTenBest)):
    print("%d. %s" % (i + 1, topTenBest[i]))

  with open("clusterRes.txt", "wb") as f:
    pickle.dump(bestClusterData, f)

  with open("clusterEvalRes.txt", "wb") as f:
    pickle.dump(avg_eval, f)

  with open("bestCluster.txt", "wb") as f:
    pickle.dump(bestCluster, f)
  
  with open("explainResults.txt", "wb") as f:
    pickle.dump(topTenBest, f)

  with open("explainValuesResults.txt", "wb") as f:
    pickle.dump(bestExplainData, f)

  with open("explainScoreAvg.txt", "wb") as f:
    pickle.dump(avg_score, f)

  with open("bestExplainValues.txt", "wb") as f:
    pickle.dump(bestExplainValues, f)
  
  with open("regularCluster.txt", "wb") as f:
    pickle.dump(regularClusters, f)

  with open("regularExplain.txt", "wb") as f:
    pickle.dump(regularExplains, f)

  if verbose:
    return bestCluster, bestExplainValues

def swaytest():
  print("Running sway test")
  # Need to add 20 runs per, grab the best val, then take the mean of the 20 best
  # exit(0)

  # best is the rows selected for being really good for sway cluster
  # data1 is the rows for the explaining algorithm
  # rule contains the rule that worked the best for this grouping
  #   Should I do an average of this if it doesn't work well? I think just extracting the features like before should be good enough but I need to pick
  #   apart the rule in depth
  #   Rule broken down:
  #     {colName: vals ... }
  #   Maybe I should save the rule to a file as well just to be safe.
  # Wrap a try except on the explainer because of the random erroring out if a rule cannot be found
  # top is the dataset that holds the best values (size determined by sway)
  bestCluster = {}
  bestClusterEvals = {}
  bestExplain = {}
  bestExplainValues = {}

  regularClusters = {}
  regularExplains = {}
  
  for i in range(20):
    print("Current run: %d" % i)
    data = DATA(config.the["file"])
    try:
      best, rest, evals = sway(data)
    except:
      continue
    config.bestNum = len(best["rows"])
    try:
      rule, most = xpln(data, best, rest)
      if rule == -1:
        continue
    except:
      continue
    data1 = DATA(data, selects(rule, data["rows"]))
    # print("all               ", stats(data)[0], stats(data, div)[0])
    # print("sway with %5s evals" % evals, stats(best)[0], stats(best, div)[0])
    # print("xpln on   %5s evals" % evals, stats(data1)[0], stats(data1, div)[0])
    top, _ = betters(data, len(best["rows"]))
    top = DATA(data, top)
    # print("sort with %5s evals" % len(data["rows"]), stats(top)[0], stats(top, div)[0])
    regularClusters[len(regularClusters)] = best["rows"]
    bestClusterEvals[len(bestClusterEvals)] = {"Evals": evals}
    bestCluster[len(bestCluster)] = stats(best)[0]
    regularExplains[len(regularExplains)] = data1["rows"]
    bestExplainValues[len(bestExplainValues)] = stats(data1)[0]
    ind = 0
    for colName, value in rule.items():
      feat = colName
      if feat in bestExplain.keys():
        bestExplain[feat] += (len(data["cols"]["names"]) - ind)
      else:
        bestExplain[feat] = len(data["cols"]["names"]) - ind
      ind += 1
      
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

  bestClusterData = getAvg(bestCluster)
  avgEval = getAvg(bestClusterEvals)["Evals"]
  print("Average of the median values for the Sway Bi-Clusterer with %5s evals over 20 runs" % avgEval, bestClusterData)

  bestExplainData = getAvg(bestExplainValues)
  print("Average of the median values for XPLN over 20 runs", bestExplainData)

  avg_eval = {avgEval}

  print("Best features extracted:")
  for i in range(len(topTenBest)):
    print("%d. %s" % (i + 1, topTenBest[i]))

  with open("clusterRes.txt", "wb") as f:
    pickle.dump(bestClusterData, f)

  with open("clusterEvalRes.txt", "wb") as f:
    pickle.dump(avg_eval, f)

  with open("bestCluster.txt", "wb") as f:
    pickle.dump(bestCluster, f)
  
  with open("explainResults.txt", "wb") as f:
    pickle.dump(topTenBest, f)

  with open("explainValuesResults.txt", "wb") as f:
    pickle.dump(bestExplainData, f)

  with open("bestExplainValues.txt", "wb") as f:
    pickle.dump(bestExplainValues, f)
  
  with open("regularCluster.txt", "wb") as f:
    pickle.dump(regularClusters, f)

  with open("regularExplain.txt", "wb") as f:
    pickle.dump(regularExplains, f)


def budgetTest():
  config.the["file"] = "../../" + config.the["file"].replace("auto93", "SSN")
  budgets = [10,25,50,100,200,500]
  base = "./budgetResults/"
  if not os.path.exists(base):
    os.mkdir(base)
  os.chdir(base)
  base = os.getcwd()

  for budget in budgets:
    if not os.path.exists(budget):
      os.mkdir(budget)
    os.chdir(budget)
    scitest(budget)
    os.chdir(base)


def autorun():
  config.the["file"] = "../../../../etc/data/project-data/auto93.csv"
  if not os.path.exists(config.resultType):
    os.mkdir(config.resultType)
  os.chdir(config.resultType)
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
    print(config.resultType)
    if config.resultType == "./results/":
      scitest()
    elif config.resultType == "./swayResults/":
      swaytest()

    os.chdir(base)
  os.chdir("../")
  print("Done autorunning")


def getResults():
  os.chdir(config.resultType)
  base = os.getcwd()
  files = ["auto2.csv", "auto93.csv", "china.csv", "coc1000.csv", "coc10000.csv", "healthCloseIsses12mths0001-hard.csv", "healthCloseIsses12mths0011-easy.csv", "nasa93dem.csv", "pom.csv", "SSM.csv", "SSN.csv"]
  results = []
  for f in files:
    directory = f.split(".")[0]
    result = []
    os.chdir("./" + directory + "/")
    
    try:
      data = DATA("curr.csv")
    except:
      data = DATA("../../../../etc/data/project-data/" + f)

    result.append(data)

    with open("clusterRes.txt", "rb") as f:
      result.append(pickle.load(f))

    with open("clusterEvalRes.txt", "rb") as f:
      result.append(pickle.load(f))

    with open("explainValuesResults.txt", "rb") as f:
      result.append(pickle.load(f))

    try:
      with open("explainScoreAvg.txt", "rb") as f:
        result.append(pickle.load(f))
    except:
      result.append({"Not Applicable"})

    with open("explainResults.txt", "rb") as f:
      result.append(pickle.load(f))
    
    with open("regularCluster.txt", "rb") as f:
      result.append(pickle.load(f))

    with open("regularExplain.txt", "rb") as f:
      result.append(pickle.load(f))
    
    os.chdir(base)
    results.append(result)

  # result = [clusterData, cluster, evals, explainData, score, explain, regularCluster, regularExplain]
  for result in results:
    data = result[0]
    print("Average of the median values for the cluster with %5s evals over 20 runs" % result[2], result[1])

    print("Average of the median values for the explainer with %5s evals over 20 runs" % result[4], result[3])

    print("Important Features:")
    for i in range(len(result[5])):
      f = result[5][i]
      print("%d. %s" % (i + 1, f))

    """
    # For debugging and looking deeper into the results
    for i in range(len(result[6])):
      resData = DATA(data, result[6][i])
      print("Median of the CLUSTERED values for the cluster with %5s evals" % result[2], stats(resData)[0], stats(resData, div)[0])
    print("ONTO EXPLAIN...")
    for i in range(len(result[7])):
      expData = DATA(data, result[7][i])
      print("Median of the CLUSTERED values for the Explain with %5s score:" % result[4], stats(expData)[0], stats(expData, div)[0])
    """
    print("----------------")


def getBothResults():
  # os.chdir(config.resultType)
  base = os.getcwd()
  files = ["auto2.csv", "auto93.csv", "china.csv", "coc1000.csv", "coc10000.csv", "healthCloseIsses12mths0001-hard.csv", "healthCloseIsses12mths0011-easy.csv", "nasa93dem.csv", "pom.csv", "SSM.csv", "SSN.csv"]
  swayResults = []
  clusterResults = []
  resultDirectories = ["./results/", "./swayResults/"]
  for file in files:
    for dire in resultDirectories:
      os.chdir(dire)
      directory = file.split(".")[0]
      result = []
      os.chdir("./" + directory + "/")
      
      try:
        data = DATA("curr.csv")
      except:
        data = DATA("../../../../etc/data/project-data/" + file)

      result.append(data)

      with open("clusterRes.txt", "rb") as f:
        result.append(pickle.load(f))

      with open("clusterEvalRes.txt", "rb") as f:
        result.append(pickle.load(f))

      with open("explainValuesResults.txt", "rb") as f:
        result.append(pickle.load(f))

      try:
        with open("explainScoreAvg.txt", "rb") as f:
          result.append(pickle.load(f))
      except:
        result.append({"Not Applicable"})

      with open("explainResults.txt", "rb") as f:
        result.append(pickle.load(f))
      
      with open("regularCluster.txt", "rb") as f:
        result.append(pickle.load(f))

      with open("regularExplain.txt", "rb") as f:
        result.append(pickle.load(f))

      with open("bestExplainValues.txt", "rb") as f:
        result.append(pickle.load(f))

      with open("bestCluster.txt", "rb") as f:
        result.append(pickle.load(f))
      
      os.chdir(base)
      if dire == "./results/":
        clusterResults.append(result)
      else:
        swayResults.append(result)

  print("done")

  for i in range(len(clusterResults)):
    cResult = clusterResults[i]
    sResult = swayResults[i]
    data = sResult[0]
    top, _ = betters(data, round(sResult[1]["N"]))
    top = DATA(data, top)
    averageTotal = stats(data)[0]
    bestTotal = stats(top)[0]
    print("Baseline for the total average of the data set", averageTotal)
    print("Average of the median values for the sway cluster with %5s evals over 20 runs" % sResult[2], sResult[1])
    print("Average of the median values for the bisect cluster with %5s evals over 20 runs" % cResult[2], cResult[1])
    print("Average of the median values for the sway explainer with %5s evals over 20 runs" % sResult[4], sResult[3])
    print("Average of the median values for the bisect explainer with %5s evals over 20 runs" % cResult[4], cResult[3])
    print("Baseline for the best group of values of the data set with %5s evals" % len(data["rows"]), bestTotal)

    print("Getting cliffsDelta effect size test results...")
    avgData = data
    bestData = top
    sway1Data = sResult[8]
    xpln1Data = sResult[9]
    sway2Data = cResult[8]
    xpln2Data = cResult[9]

    try:
      print("Diff in all vs all")
      cols = {}
      for k in averageTotal.keys():
        # Format needed for average and top. xpln and sway would need similar - the colnames stuff since it should just key match k
        val1 = {}
        ind = 0
        for colName in cols["cols"]["names"]:
          if colName.rstrip() == k:
            break
          ind += 1
        for row in avgData["rows"]:
          val1[len(val1)] = row[i]

        if cliffDelta(val1, val1):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing all vs all")
      pass

    # Above def needs debugging
    continue
    try:
      print("Diff in all vs sway1")
      cols = {}
      for k, v in averageTotal.items():
        if cliffDelta(v, sResult[1][k]):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing all vs sway1")
      pass

    try:
      print("Diff in all vs sway2")
      cols = {}
      for k, v in averageTotal.items():
        if cliffDelta(v, cResult[1][k]):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing all vs sway2")
      pass

    try:
      print("Diff in sway1 vs sway2")
      cols = {}
      for k, v in sResult[1].items():
        if cliffDelta(v, cResult[1][k]):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing sway1 vs sway2")
      pass

    try:
      print("Diff in sway1 vs xpln1")
      cols = {}
      for k, v in sResult[1].items():
        if cliffDelta(v, sResult[3][k]):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing sway1 vs sway2")
      pass

    try:
      print("Diff in sway2 vs xpln2")
      cols = {}
      for k, v in cResult[1].items():
        if cliffDelta(v, cResult[3][k]):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing sway2 vs xpln2")
      pass

    try:
      print("Diff in sway1 vs top")
      cols = {}
      for k, v in sResult[1].items():
        if cliffDelta(v, bestTotal[k]):
          cols[k] = "!="
        else:
          cols[k] = "="
      print("cols vals:", cols)
    except KeyError:
      print("Error in printing sway1 vs top")
      pass
    
    print("----------------")


def getBenchmarks():
  file_info = {"auto2.csv": 6, "auto93.csv": 12, "china.csv": 16, "coc1000.csv":19, "coc10000.csv": 79, "healthCloseIsses12mths0001-hard.csv": 79, "healthCloseIsses12mths0011-easy.csv": 79, "nasa93dem.csv": 6, "pom.csv": 79, "SSM.csv": 468, "SSN.csv": 209}
  for file, number in file_info.items():
    data = DATA(config.the["file"].replace("auto93.csv", file))
    top, _ = betters(data, number)
    top = DATA(data, top)
    print("Baseline for the total average of the data set with %5s evals" % len(data["rows"]), stats(data)[0])
    print("Baseline for the best group of values of the data set", stats(top)[0])
    print("-----------------")