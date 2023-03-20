import re
import sys


def augSort(d, fun=None):
    # My augmented sort function to handle the difference between lua tables and python dicts
    lst = []
    for _, item in d.items():
        lst.append(item)
    if fun is None:
      lst.sort()
    else:
      lst.sort(key=fun)
    nd = {}
    for i in range(len(lst)):
        nd[i] = lst[i]
    return nd


def RX(t,s=""):
    # sorts and returns the data of t in num format
    t = augSort(t)
    return {"name": s, "rank": 0, "n": len(t), "show": "", "has": t}


def merge(rx1, rx2):
    # Merges two "buckets"
    rx3 = RX({}, rx1["name"])
    for _, item in rx1["has"].items():
        rx3["has"][len(rx3["has"])] = item
    for _, item in rx2["has"].items():
        rx3["has"][len(rx3["has"])] = item
    rx3["has"] = augSort(rx3["has"])
    rx3["n"] = len(rx3["has"])
    return rx3


def con(d, std=1):
  # Concatinates items in d
  s = ""
  if std == 1:
    for _, item in d.items():
      s += item
  else:
    for i in range(len(d)):
      s += str(d[i])
  return s


def coerce(s):
  # Convert to python data types from strings
  def fun(s1):
    if s1 == "true" or s1 == "True":
      return True
    elif s1 == "false" or s1 == "False":
      return False
    else:
      return s1
  if type(s) == bool:
    return s
  try:
    res = int(s)
  except:
    try:
      res = float(s)
    except:
      res = fun(re.match("^\s*(.+)\s*$", s).string)
  return res


def settings(s):
  # Parses the help to get possible the command line arguements
  t={}
  res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
  for k,v in res:
    t[k] = coerce(v)
  return t


def cli(options):
  # Parses the settings parse to put into python understandable form
  for k,v in options.items():
    v = str(v)
    for n, x in enumerate(sys.argv):
      if (x == ("-" + k[0:1])) or (x == ("--" + k)):
        more = False
        try: 
          sys.argv[n+1]
          v = sys.argv[n+1]
          break
        except:
          more = False
        v = v == "False" and True or v == "True" and False or more
    options[k] = coerce(v)
  return options