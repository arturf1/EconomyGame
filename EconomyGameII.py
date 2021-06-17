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

def generateMaterialDistribution(M,d,totalDays):
    distribution = []
    for m in range(len(M)):
        distribution.append(math.exp(-abs(m/len(M)-d/totalDays)*len(M)))
    distribution = distribution / np.sum(distribution)
    return distribution

def createContract(M, dist, lenght):
    contract = []
    # ensure first two elements are different
    random.choices(M, weights=dist, )

    return np.random.choice(M,lenght,replace=False, p=dist)

def getContractInitValue(M, dist, contract):
    prop = 1
    for m in contract:
        prop = prop*dist[M.index(m)]
    return 1/prop

def getContractValue(initalValue, marketSaturationSpeed):
    i = 0 
    value = 0 
    while(initalValue*math.exp(-(i)*marketSaturationSpeed) > 1):
        value += initalValue*math.exp(-(i)*marketSaturationSpeed)
        i += 1
    return value

def fillContract(storage, contract, qty, price, M):
    neededMaterials = []
    for m in M: 
        neededMaterials.append(list(contract).count(m))
    
    leftovers = np.array(storage) - qty*np.array(neededMaterials)

    if (np.sum(leftovers < 0) or price < 1 ):
        return storage, 0
    else:
        return list(leftovers), price*qty
        
def getPrice(initalValue, numberFulfilled, marketSaturationSpeed):
    return initalValue*math.exp(-(numberFulfilled)*marketSaturationSpeed)

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
    moveMineCost = -np.sum(change[np.where(change < 0)])*move_mine_cost
    return newMineCost + moveMineCost

# Materials & rates 
M = ["Wood", "Stone", "Copper", "Bronze", "Iron", "Concrete", "Steel", "Platics", "Graphine", "Superconductors"]
marketSaturationSpeed = 0.5
totalDays = 50
currentContract = []
currentContractFills = 0
currentContractInitVal = 0
balance = 1500

prodDist = np.zeros(len(M))
storage = np.zeros(len(M))
storage_cost = 10
prod_per_day = 10
new_mine_cost = 1000
move_mine_cost = 100
costs = np.zeros(2)

dist = generateMaterialDistribution(M,0,totalDays)
currentContract = createContract(M, dist, 2)
currentContractInitVal = getContractInitValue(M, dist, currentContract)

for d in range(0,totalDays):
    clear()
    print("Materials " + str(M))
    print("Balance: $%.2f " % (balance))
    print("\n")

    r = getPrice(currentContractInitVal, currentContractFills, marketSaturationSpeed)
    print ("Current Contract: " + str(currentContract) + " Next sale: $%.2f" % r)
    print("Storage")
    print (storage)

    print("Set new production")
    cmd = input()
    if (cmd != ""):
        newProdDist = np.fromstring(cmd, sep=" ")
        costs[1] += productionChangeCost(newProdDist, prodDist, new_mine_cost, move_mine_cost)
        prodDist = newProdDist
        print("Production change cost -$%.2f" % (costs[1]))
    
    print("Mine Distribution")
    print(prodDist)

    print("Storage")
    storage += produce(prodDist,prod_per_day)
    print(storage)

    print("Fill contract?")
    cmd = input()
    while(cmd != "n"):
        p  = getPrice(currentContractInitVal, currentContractFills, marketSaturationSpeed)
        storage, revenue = fillContract(storage, currentContract, 1, p, M)
        if (revenue != 0):
            currentContractFills += 1
            balance += revenue
            print("Sale %d: $%.2f " % (currentContractFills,p))
            print("Balance: $%.2f " % (balance))
            cmd = input()
        else:
            print("Unable to fill contract.")
            cmd = "n"

    print("Generate a new contract? (Warning: penalty = last sale price)")
    cmd = input()
    if (cmd == 'y'):
        balance  -= getPrice(currentContractInitVal, currentContractFills, marketSaturationSpeed)
        dist = generateMaterialDistribution(M,d,totalDays)
        currentContract = createContract(M, dist, 2)
        currentContractFills = 0
        currentContractInitVal = getContractInitValue(M, dist, currentContract)
 
    costs[0] += storage_cost*np.sum(storage)
    balance = balance - costs[0] - costs[1]
    