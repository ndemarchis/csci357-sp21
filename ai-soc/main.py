import requests
import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt

newImgsToCheck = 50

count = 0
nsfwDict = {}
x = []
y = []

UTKDict = {
    "gender": {
        "0": "M", 
        "1": "F"
    },
    "race": {
        "0": "W",
        "1": "B",
        "2": "A",
        "3": "A",
        "4": "L",
    }
}

intersectionalDict = {"CFD": {}, "UTKFace": {}}
genderDict = {"CFD": {}, "UTKFace": {}}
raceDict = {"CFD": {}, "UTKFace": {}}


outputFileName = "./ai-soc/data/data.json"

if os.path.exists(outputFileName):
    with open(outputFileName) as f:
        nsfwDict = json.load(f)


def makeRequest(path):
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            'image': open(path, 'rb'),
        },
        # headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        headers={'api-key': 'a35e4cbf-3de7-420a-8eee-16f3bbd24284'}
    )
    print(r.json())
    return (r.json()["output"]["nsfw_score"])

def parseData(obj):

    intersection = obj['race'] + obj['gender']
    handleDictEntry(raceDict, obj, obj['race'])
    handleDictEntry(genderDict, obj, obj['gender'])
    handleDictEntry(intersectionalDict, obj, intersection)

def handleDictEntry(dict, obj, attribute):
    if attribute not in dict[obj['database']]:
        dict[obj['database']][attribute] = [obj["score"]]
        pass
    else:
        dict[obj['database']][attribute].append(obj["score"])
        pass

def zippy(keys, data):
    zipped = zip(keys, data)
    sortedZipped = sorted(zipped)
    sortedKeys = sorted(keys)
    sortedData = [element for _, element in sortedZipped]
    return sortedKeys, sortedData

def createGraph(dicty):
    CFDData = []
    CFDKeys = []
    UTKData = []
    UTKKeys = []

    for databases in dicty:
        for key in dicty[databases]:
            if (databases == "CFD"):
                CFDKeys.append(key)
                CFDData.append(dicty[databases][key])
            elif (databases == "UTKFace"):
                UTKKeys.append(key)
                UTKData.append(dicty[databases][key])                

    CFDKeys, CFDData = zippy(CFDKeys, CFDData)
    UTKKeys, UTKData = zippy(UTKKeys, UTKData)

    fig = plt.figure()

    ax1 = fig.add_subplot(211)
    plt.boxplot(CFDData, showfliers=False)
    ax1.set_xticklabels(CFDKeys)
    ax1.set_title("Chicago Face Database")

    ax2 = fig.add_subplot(212)
    plt.boxplot(UTKData, showfliers=False)
    ax2.set_xticklabels(UTKKeys)
    ax2.set_title("UTKFace")
    plt.show()

for root, dirs, files in os.walk("ai-soc/test images"):
    for f in files:
        if f not in nsfwDict:
            temp = (os.path.relpath(os.path.join(root, f), "."))
            if ((".jpg" in temp) and (count < newImgsToCheck)):
                if (("CFD" in temp) and ("LF" in temp)):
                    print(f)
                    request = makeRequest(temp)
                    nsfwDict[f] = {
                        'database': "CFD",
                        'fullPath': temp,
                        'score': request,
                        'race': f[4],
                        'gender': f[5],
                        'modelId': f[7:10],
                        'imageId': f[11:14],
                        'expression': f[15:-4],
                    }
                    count += 1
                    pass
                elif ("UTKFace" in temp):
                    print(f)
                    close = f[:(len(f) - 31)]
                    age = int(close[0:-4])
                    if ((age >= 20) and (age <= 30)):
                        request = makeRequest(temp)
                        tempObj = {
                            'database': "UTKFace",
                            'fullPath': temp,
                            'score': request,
                            'race': UTKDict["race"][close[-1]],
                            'gender': UTKDict["gender"][close[-3]],
                            'age': age,
                        }
                        nsfwDict[f] = tempObj
                        count += 1
                    pass
    
for key in nsfwDict:
    parseData(nsfwDict[key])

print(count)

with open(outputFileName, 'w') as fp:
    json.dump(nsfwDict, fp, indent=4)

createGraph(intersectionalDict)