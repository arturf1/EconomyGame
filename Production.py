import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 14
plt.rcParams['toolbar'] = 'None'
from matplotlib.ticker import FormatStrFormatter
import pandas as pd

import os
from scipy.stats import cauchy
import random
import math

clear = lambda: os.system('cls')

def produce(prodDist, totalProduct):
    result = np.zeros(len(prodDist))
    result += math.floor(totalProduct/np.sum(prodDist))*prodDist
    if (np.sum(result) != totalProduct):
        i = 0 
        while (np.sum(result) != totalProduct):
            remaining = np.sum(result) - totalProduct
            if (remaining >= prodDist[i]):
                result[i] += prodDist[i]
            else:
                result[i] += remaining
                break

    return result

def productionChangeCost(newProdDist, oldProdDist, new_mine_cost, move_mine_cost):
    newMineCost = (np.sum(newProdDist) - np.sum(oldProdDist))*new_mine_cost
    change = newProdDist - oldProdDist
    print(change)
    print(newProdDist)
    moveMineCost = -np.sum(change[np.where(change < 0)])*move_mine_cost
    return newMineCost + moveMineCost


# Materials & rates 
M = ["Wood", "Stone", "Copper", "Bronze"]
prodDist = np.zeros(len(M))
prodDist[0] = 1
storage = np.zeros(len(M))
storage_cost = 10
new_mine_cost = 1000
move_mine_cost = 100
costs = np.zeros(2)

totalDays = 50
for d in range(0,totalDays):
    clear()

    print("Mine Distribution " + str(M))
    print(prodDist)

    print("Storage " + str(M))
    storage += produce(prodDist,100)
    print(storage)

    print("Cost Storage -$%.2f | Production -$%.2f" % (costs[0], costs[1]))
    costs[0] += storage_cost*np.sum(storage)

    cmd = input()
    if (cmd != "n"):
        print(cmd)
        newProdDist = np.fromstring(cmd, sep=" ")
        costs[1] += productionChangeCost(newProdDist, prodDist, new_mine_cost, move_mine_cost)
        prodDist = newProdDist
        
    