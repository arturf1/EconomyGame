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

def getRevenue(initalValue, numberFulfilled, marketSaturationSpeed):
    return initalValue*math.exp(-(numberFulfilled)*marketSaturationSpeed)

def getContractValue(initalValue, marketSaturationSpeed):
    i = 0 
    value = 0 
    while(initalValue*math.exp(-(i)*marketSaturationSpeed) > 1):
        value += initalValue*math.exp(-(i)*marketSaturationSpeed)
        i += 1
    return value

fills = 50
initalValue = 3000
marketSaturationSpeed = initalValue / 1000
n = 0
s = 0
clear()

print("Total value: $%.2f " % (getContractValue(initalValue, marketSaturationSpeed)))

for d in range(0,fills):
    r = getRevenue(initalValue, n, marketSaturationSpeed)
    s += r
    n += 1
    print("Sale %d: $%.2f " % (n,r))
    print("Total: $%.2f " % (s))
    input()

        

# Value 
# Price 
# Units 
# V = 0.5 * P * U
# Prob 
# 