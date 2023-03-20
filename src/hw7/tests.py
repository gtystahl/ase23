from classes import *
from helpers import *
from statFunctions import *
import config
import random

# This is the file that holds the functions for all of the tests


def ok():
  # Sets the random seed to 1
  random.seed = 1


def sample():
  # Tests getting a sample of items from a dict
  for i in range(10):
     print("", con(samples({0: "a", 1: "b", 2: "c", 3: "d", 4: "e"})))


def num():
  # Tests the number creator function
  n = NUM({0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10})
  print("", n["n"], n["mu"], n["sd"])


def gauss():
  # Tests the gaussian function
  t = {}
  for i in range(10**4):
    t[len(t)] = gaussian(10, 2)
  n = NUM(t)
  print("", n["n"], n["mu"], n["sd"])


def bootmu():
  # Tests the bootstrapping function
  a = {}
  b = {}
  for i in range(100):
    a[len(a)] = gaussian(10, 1)
  print("","mu","sd","cliffs","boot","both")
  print("","--","--","------","----","----")
  for iter in range(0, 11):
    mu = 10 + (0.1 * iter)
    b = {}
    for i in range(100):
      b[len(b)] = gaussian(mu, 1)
    cl = cliffsDelta(a,b)
    bs = bootstrap(a,b)
    print("",mu,1,cl,bs,cl and bs)


def pre():
  # Tests the Bottstrap and Gausian functions again
  print("\neg3")
  d = 1
  for i in range(10):
    t1 = {}
    t2 = {}
    for j in range(32):
      t1[len(t1)] = gaussian(10, 1)
      t2[len(t2)] = gaussian(d * 10, 1)
    print("\t",d,"true" if d<1.1 else "false",bootstrap(t1,t2),bootstrap(t1,t1))
    d = d + 0.05


def five():
  # Tests scott knot
  inp = {
         0: RX({0: 0.34, 1: 0.49, 2: 0.51, 3: 0.6,  4: .34,  5: .49,  6: .51, 7: .6},"rx1"),
         1: RX({0: 0.6,  1: 0.7,  2: 0.8,  3: 0.9,  4: .6,   5: .7,   6: .8,  7: .9},"rx2"),
         2: RX({0: 0.15, 1: 0.25, 2: 0.4,  3: 0.35, 4: 0.15, 5: 0.25, 6: 0.4, 7: 0.35},"rx3"),
         3: RX({0: 0.6,  1: 0.7,  2: 0.8,  3: 0.9,  4: 0.6,  5: 0.7,  6: 0.8, 7: 0.9},"rx4"), 
         4: RX({0: 0.1,  1: 0.2,  2: 0.3,  3: 0.4,  4: 0.1,  5: 0.2,  6: 0.3, 7: 0.4},"rx5")
        }
  res1 = scottKnot(inp)
  res2 = tiles(res1)
  for _, rx in res2.items():
    print(rx["name"],rx["rank"],rx["show"])
   

def six():
  # Tests scott knot again
  for _,rx in tiles(scottKnot({
         0: RX({0: 101, 1: 100, 2: 99,   3: 101, 4: 99.5, 5: 101, 6: 100, 7: 99,   8: 101, 9: 99.5},"rx1"),
         1: RX({0: 101, 1: 100, 2: 99,   3: 101, 4: 100,  5: 101, 6: 100, 7: 99,   8: 101, 9: 100},"rx2"),
         2: RX({0: 101, 1: 100, 2: 99.5, 3: 101, 4: 99,   5: 101, 6: 100, 7: 99.5, 8: 101, 9: 99},"rx3"),
         3: RX({0: 101, 1: 100, 2: 99,   3: 101, 4: 100,  5: 101, 6: 100, 7: 99,   8: 101, 9: 100},"rx4")})).items():
    print(rx["name"],rx["rank"],rx["show"])


def til():
  # Tests printing the tiles
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i in range(1000): 
    a[len(a)] = gaussian(10,1)
  for i in range(1000): 
    b[len(b)] = gaussian(10.1,1)
  for i in range(1000): 
    c[len(c)] = gaussian(20,1)
  for i in range(1000): 
    d[len(d)] = gaussian(30,1)
  for i in range(1000): 
    e[len(e)] = gaussian(30.1,1)
  for i in range(1000): 
    f[len(f)] = gaussian(10,1)
  for i in range(1000): 
    g[len(g)] = gaussian(10,1)
  for i in range(1000): 
    h[len(h)] = gaussian(40,1)
  for i in range(1000): 
    j[len(j)] = gaussian(40,3)
  for i in range(1000): 
    k[len(k)] = gaussian(10,1)

  for k,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
    rxs[k] =  RX(v,"rx" + str(k))
  rxs = augSort(rxs, mid)
  for _,rx in tiles(rxs).items():
    print("",rx["name"],rx["show"])


def sk():
  # Tests printing the tiles with scotts knot
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i in range(1000): 
    a[len(a)] = gaussian(10,1)
  for i in range(1000): 
    b[len(b)] = gaussian(10.1,1)
  for i in range(1000): 
    c[len(c)] = gaussian(20,1)
  for i in range(1000): 
    d[len(d)] = gaussian(30,1)
  for i in range(1000): 
    e[len(e)] = gaussian(30.1,1)
  for i in range(1000): 
    f[len(f)] = gaussian(10,1)
  for i in range(1000): 
    g[len(g)] = gaussian(10,1)
  for i in range(1000): 
    h[len(h)] = gaussian(40,1)
  for i in range(1000): 
    j[len(j)] = gaussian(40,3)
  for i in range(1000): 
    k[len(k)] = gaussian(10,1)
  for k,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
    rxs[k] =  RX(v,"rx" + str(k))
  for _,rx in tiles(scottKnot(rxs)).items():
    print("",rx["rank"],rx["name"],rx["show"])