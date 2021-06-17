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

def createContract(M):
    contract = []
    lenght = random.randint(2, 3)
    # ensure first two elements are different
    first_element = [random.choice(M)]
    contract.append(first_element[0])
    contract.append(random.choice([x for x in M if x not in first_element]))
    for i in range(lenght-2):
        contract.append(random.choice(M))
    return contract


def generateContracts(M, n):
    contracts = []
    count = 0 
    similar_contract = False
    while (count < n):
        c = createContract(M)
        for contract in contracts:
            if (set(contract) == set(c)):
                similar_contract = True
                break
        
        if not similar_contract:
            contracts.append(c)
            count += 1
        else:
            similar_contract = False

    return contracts

def getBasicContractValue(contract, M, r):
    value = 0
    for m in contract:
        value += 1/r[M.index(m)]
    return value

def priceContracts(contracts, M, r):
    prices = []
    for contract in contracts:
        v = getBasicContractValue(contract, M, r)
        # sigma should be set considering how often very good contracts should appear
        # this would be a function of lenght of the game and number of contracts per day
        # set such that P(ln > 3) = 0.05
        sigma = 0.5
        # mean exp(mu + sig^2/2) = 1
        # ln = np.random.lognormal(-sigma**2/2, sigma)
        # mode exp(mu - sig^2) = 1
        ln = np.random.lognormal(sigma**2, sigma)
        p = v*ln
        prices.append(round(p, 0))
    return prices

def addMaterial(storage, time, m, qty, M, r):
    if qty/r[M.index(m)] > time:
        storage[M.index(m)] += math.floor(r[M.index(m)]*time)
        time -= math.floor(r[M.index(m)]*time)/r[M.index(m)]
    else:
        storage[M.index(m)] += qty
        time -= qty/r[M.index(m)]

    return storage, time

def fillContract(storage, contract, qty, price, M):
    neededMaterials = []
    for m in M: 
        neededMaterials.append(contract.count(m))
    
    leftovers = np.array(storage) - qty*np.array(neededMaterials)

    if (np.sum(leftovers < 0)):
        return storage, 0
    else:
        return list(leftovers), price*qty

def validMineCommand(command, M):
    if len(command) != 2:
        return False 
    if command[0] not in M: 
        return False
    if not command[1].isdigit():
        return False 
    
    return True

def validFillCommand(command):
    if len(command) != 2:
        return False 
    if not command[0].isdigit(): 
        return False
    if not command[1].isdigit():
        return False 
    
    return True

# Materials & rates 
M = ["R", "G", "B", "Y", "W"]
r = [1/10, 1/15, 1/30, 1/60, 1/100]
storage = np.zeros(len(M))
balance = 0 

for d in range(0,5):
    clear()
    time = 600
    contracts = generateContracts(M, 5)
    prices = priceContracts(contracts, M, r)

    print("Materials " + str(M))
    print("Mining rates (units per day) " + str(time*np.array(r)))
    #print("Lenght of day: " + str(time))
    print("\n")

    #print("Your storage")
    #print("Materials " + str(M))
    #print(storage)
    #print("Bank balance $%0.2f" % balance)
    #print("\n")

    print("Day " + str(d+1) + "/5")
    print("Today's contracts")
    for c, p in zip(contracts, prices):
        print(str(c) + " " + "$" + str(int(p)) + " (%.2f)" % (p/getBasicContractValue(c, M, r)))
    
    #print("\nPick resource to mine today")
    #input1 = ''
    input1 = input()
    """m = input1
    if (m in M):
        storage, time = addMaterial(storage, 600, m, 9999, M, r)
        print("Current storage: " + str(storage))
    
    print("\nInput command ('Contract# QTY' or 'Done')")
    input1 = ''     
    while(input1 != "Done"):
        input1 = input()
        command = input1.split(' ')
        if (validFillCommand(command)):
            storage, revenue = fillContract(storage, contracts[int(command[0])-1], int(command[1]), prices[int(command[0])-1], M)
            balance += revenue
            print("Current storage: " + str(storage))
            print("Bank balance $%0.2f" % balance)"""
        
# Scores 
# 1. $3548.90
# 2. $3336.95
# 3. $3325.63
# 4. $3248.47