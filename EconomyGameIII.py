import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 10
plt.rcParams['toolbar'] = 'None'
from matplotlib.ticker import FormatStrFormatter

import os
from scipy.stats import cauchy
import random
import math
import itertools

clear = lambda: os.system('cls')

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
    distribution = distribution / np.sum(distribution)
    random.shuffle(distribution)
    return distribution

def createContract(M, dist, lenght):
    contract = []
    random.choices(M, weights=dist)
    return np.random.choice(M,lenght,replace=True, p=dist)

def getContractProbability(M, dist, contract):
    prob = 1
    for m in contract:
        prob *= dist[M.index(m)]
    return prob

def getContractValue(M, dist, contract):
    # Number of mine switches expacted
    unique_elem = np.unique(np.array(contract)).shape[0]
    
    # Number of days excess materials need to be stored
    s = 0 
    for m in contract:
        prop = 1 - math.pow((1-dist[M.index(m)]),len(contract))
        s += (1/prop)

    return round((10*s)/10)*10

def expectedDailyRevenue(M, dist, lenght):
    revenue = 0
    contracts = itertools.product(M, repeat=lenght) 
    for contract in list(contracts): 
        revenue += getContractProbability(M, dist, contract)*getContractValue(M, dist, contract) 
    return revenue

def fillContract(storage, contract, qty, price, M):
    neededMaterials = []
    for m in M: 
        neededMaterials.append(list(contract).count(m))
    
    leftovers = np.array(storage) - qty*np.array(neededMaterials)

    if (np.sum(leftovers < 0) or price < 1 ):
        return storage, 0
    else:
        return list(leftovers), price*qty

def mine(M, order, mine_rate, storage):
    amount = random.randint(1,mine_rate+1)
    storage[M.index(order)] += amount
    return storage, amount

def printStorage(M, storage):
    msg = ""
    for m in M:
        msg += "% 3d %s  " % (storage[M.index(m)], m)
    print(msg)

def storageCost(storage, storage_cost):
    return storage_cost*np.sum(storage)
 
M = ["Wood", "Stone", "Copper", "Bronze", "Iron", "Concrete", "Steel", "Plastics", "Graphine"]
MINE_RATE_PER_DAY = 2
TOTAL_DAYS = 50

currentContract = []
currentContractFills = 0
storage = np.zeros(len(M))
cost = 0

plt.ion()
fig = plt.figure()
balances = []
costs = []

dist = generateMaterialDistribution(M)
currentContract = createContract(M, dist, 2)

ER = expectedDailyRevenue(M, dist, 2)
DAILY_OPS_COST = round(0.25*ER)
STORAGE_COST = round(0.75*ER/len(M))
SKIP_CONTRACT_PENALTY = 0.1

# enough start money for
DAYS_FOR_EXPLORATION = 5 
balance = DAYS_FOR_EXPLORATION*DAILY_OPS_COST + DAYS_FOR_EXPLORATION*SKIP_CONTRACT_PENALTY*ER
balance = round(balance/10)*10

for d in range(0,TOTAL_DAYS):
    clear()
    print("Storage cost per unit: -$%.2f | Daily operating cost: -$%.2f" % (STORAGE_COST, DAILY_OPS_COST))
    print("Storage (Yesterday's cost -$%.2f)" % storageCost(storage, STORAGE_COST))
    printStorage(M, storage)
    print("Balance: $%.2f " % (balance))
    print("Yesterday's total cost: -$%.2f " % (cost))
    print("")

    r = getContractValue(M, dist, currentContract)
    print ("Current Contract: " + str(currentContract) + " Price: $%.2f " % (r))
    print ("(Skip Cost: $%.2f | Possible Profit: $%.2f )" % (SKIP_CONTRACT_PENALTY*r, r-cost))
    print("")

    cost = 0

    order = ""
    while (order not in M and order != 'n'):
        print("What would you like to mine?")
        order = input()
    if (order in M):
        storage, amount = mine(M, order, MINE_RATE_PER_DAY, storage)
        print("Mined %d %s" % (amount, order))

    print("Fill contract? (y/n)")
    cmd = input()
    if(cmd != "n" and currentContractFills == 0):
        p  = getContractValue(M, dist, currentContract)
        storage, revenue = fillContract(storage, currentContract, 1, p, M)
        if (revenue != 0):
            currentContractFills += 1
            balance += revenue
            print("Sale %d: $%.2f " % (currentContractFills,p))
        else:
            print("Unable to fill contract.")
            cmd = "n"

    if (currentContractFills != 1):
        print("Generate a new contract (y/n)? (Warning: penalty = 10%*price)")
        cmd = input()
    if (cmd == 'y' or currentContractFills == 1):
        cost  += SKIP_CONTRACT_PENALTY*getContractValue(M, dist, currentContract)*(1-currentContractFills)
        currentContract = createContract(M, dist, 2)
        currentContractFills = 0
        currentContractInitVal = getContractValue(M, dist, currentContract)
 
    cost += storageCost(storage, STORAGE_COST)
    cost += DAILY_OPS_COST
    balance = balance - cost
    
    balances.append(balance)
    costs.append(cost)

    fig.clear()
    plt.plot(balances, c="g", label="Balance")
    plt.plot(costs, c="r", label="Storage Cost")
    plt.ylabel("$")
    plt.xlabel("Day")
    plt.legend()
    fig.canvas.draw()

    print("Balance: $%.2f " % (balance))
    print("Press Enter to Continue...")
    input()
    