import math
import random
import config
from helpers import *

# This file contains all of the stat functions made to analyse the data


def erf(x):
    # Function from Abramowitz and Stegun
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5 * t + a4)*t) + a3)*t + a2)*t + a1)*t * math.exp(-x*x)

    return sign * y


def gaussian(mu=0, sd=1):
    # Return a sampe from a guassian with mean and standard deviation
    sq = math.sqrt
    pi = math.pi
    log = math.log
    cos = math.cos
    r = random.random
    return mu + sd * sq(-2*log(r())) * cos(2*pi*r())


def samples(t, n=0):
    # Gets n samples from t
    if n is None or n == 0:
        n = len(t)
    u = {}
    for i in range(n):
        u[i] = t[random.randint(0, n - 1)]
    return u


def cliffsDelta(ns1, ns2):
    # True if different by a trivial amount
    if len(ns1) == 0 or len(ns2) == 0:
        return False
    n = 0
    gt = 0
    lt = 0

    if len(ns1) > 128:
        ns1 = samples(ns1, 128)
    if len(ns2) > 128:
        ns2 = samples(ns2, 128)
    
    for a in range(len(ns1)):
        x = ns1[a]
        for b in range(len(ns2)):
            y = ns2[b]
            n = n + 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1
    return abs(lt - gt)/n <= config.the["cliff"]