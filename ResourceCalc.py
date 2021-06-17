import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 14
plt.rcParams['toolbar'] = 'None'
from matplotlib.ticker import FormatStrFormatter
import pandas as pd

import os
import random

clear = lambda: os.system('cls')

# Materials & rates 
M = ["R", "G", "B"]
r = [1/10, 1/30, 1/60]

while True:
    clear()

    print("Materials " + str(M))
    print("Mining rates (per unit) " + str(1/np.array(r)))
    print("Lenght of day: 600")
    print("\n")

    input1 = input()
    m = np.fromstring(input1, sep=" ")
    print(m)
    print("Total time cost: " + str(np.sum(m/np.array(r))))
    input()