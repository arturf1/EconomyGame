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

'''
def generateMaterialDistribution(M,d,totalDays):
    distribution = []
    for m in range(len(M)):
        distribution.append(math.exp(-abs(m/len(M)-d/totalDays)*len(M)))
    distribution = distribution / np.sum(distribution)
    return distribution'''

def generateMaterialDistribution(M):
    distribution = []
    i = 0
    j = 0
    for m in range(len(M)):
        if (j >= (len(M)+1)/2):
            i -= 1
        else:
            i += 1
        j += 1
        distribution.append(i)
    print(distribution)
    distribution = distribution / np.sum(distribution)
    random.shuffle(distribution)
    return distribution

def createContract(M, dist, lenght):
    contract = []
    # ensure first two elements are different
    random.choices(M, weights=dist, )

    return np.random.choice(M,lenght,replace=True, p=dist)

'''
def getContractInitValue(M, dist, contract):
    prop = 1
    for m in contract:
        prop = prop*dist[M.index(m)]
    
    x = np.partition(dist, -2)[-2]
    y = np.max(dist)
    print(x*y/prop)
    return 1/prop

def getContractValue(initalValue, marketSaturationSpeed):
    i = 0 
    value = 0 
    while(initalValue*math.exp(-(i)*marketSaturationSpeed) > 1):
        value += initalValue*math.exp(-(i)*marketSaturationSpeed)
        i += 1
    print(i)
    return value
'''

def getContractInitValue(M, dist, contract):
    prop = 1
    for m in contract:
        prop = prop*dist[M.index(m)]
    return 1/prop

def getContractValue(M, dist, contract):
    C_M = 10
    C_S = 10

    # Number of mine switches expacted
    unique_elem = np.unique(np.array(contract)).shape[0]
    
    # Number of days excess materials need to be stored
    s = 0 
    for m in contract:
        prop = 1 - math.pow((1-dist[M.index(m)]),len(contract))
        s += (1/prop)
    
    print(C_M*unique_elem)
    print(C_S*s)
    return C_M*unique_elem + C_S*s

# Materials & rates 
M = ["Wood", "Stone", "Copper", "Bronze", "Iron", "Concrete", "Steel", "Platics", "Graphine"]
marketSaturationSpeed = 0.5
totalDays = 50

for d in range(0,totalDays):
    clear()

    print("Materials " + str(M))
    #dist = generateMaterialDistribution(M,d,totalDays)
    dist = generateMaterialDistribution(M)
    print(dist)

    for i in range(50):
        contract = createContract(M, dist, 2)
        value = getContractInitValue(M, dist, contract)
        print(str(contract) + " Value $%0.2f | Value $%0.2f"  % (value, getContractValue(M, dist, contract)))
    
    input()
    