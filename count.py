import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 14
plt.rcParams['toolbar'] = 'None'
from matplotlib.ticker import FormatStrFormatter
import pandas as pd

def count(item, counts):
    if (item in counts.keys()):
        counts[item] += 1
    
    return counts

def update_graph(counts):
    fig.clear()
    keys = counts.keys()
    values = counts.values()
    plt.bar(keys, values, color=plt.cm.get_cmap("hsv", 10)(np.random.random_integers(0,9)))
    plt.ylabel('Votes')
    plt.ylim([0, round(1.1*max(values)+1)])
    plt.draw()
    plt.pause(0.001)

fig, ax = plt.subplots()
counts = {"item" : 0, "test" : 0, "aaa" : 0}
plt.show(block=False)

with open('./test.txt') as f:
    for line in f:
        item = line[:-1]
        counts = count(item, counts)
        update_graph(counts)

top_action = max(counts, key=counts.get)
print(top_action)
plt.show()