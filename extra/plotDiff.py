import json
import numpy as np
import matplotlib.pyplot as plt
import sys
from decimal import Decimal

datafile = sys.argv[1]

numLines = sum(1 for line in open(datafile))

file = open(datafile,"r")
dataDict = {}

for line in file:
    try:
        jsonLine = json.loads(line)
        meas = jsonLine['meas']
        for anchor in meas:
            if anchor['addr'] not in dataDict:
                array = [None] * numLines
                dataDict[anchor['addr']] = array
    except (ValueError, KeyError) as e:
        pass

file.close()
file = open(datafile,"r")

errors = 0
for index, line in enumerate(file):
    try:
        jsonLine = json.loads(line)
        meas = jsonLine['meas']
        for anchor in meas:
            dataDict[anchor['addr']][index] = anchor['ddist']
    except (ValueError, KeyError) as e:
        errors = errors +1
        print(e)
        print(line)
        print(errors)
        pass


colors = ['blue', 'red','yellow','black','purple','green','Orange','black']
for index,key in enumerate(dataDict.keys()):
    datan = [x for x in dataDict[key] if x is not None]
    data = map(float,datan)
    var = str(np.var(data))
    mean = str(np.mean(data))
    plt.plot(dataDict[key],label=key+", var: "+var[0:7] +", mean: "+mean[0:7],color=colors[index])
    plt.legend(loc='upper left')
    
#plt.plot(dataDict["4930"])
plt.show()
