import json
import numpy as np
import matplotlib.pyplot as plt


datafile = "ryssdata/log_ddist.txt"

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
    plt.plot(dataDict[key],label=key,color=colors[index])
    plt.legend(loc='upper left')
#plt.plot(dataDict["4930"])
plt.show()