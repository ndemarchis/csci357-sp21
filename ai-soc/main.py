import requests
import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt

newImgsToCheck = 1

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
        "4": "M",
    }
}

intersectionalDict = {}
genderDict = {}
raceDict = {}

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

    x.append(int(re.sub("[^0-9]", "", obj["imageId"])))
    y.append(float(obj["score"]))

def handleDictEntry(dict, obj, attribute):
    if attribute not in dict:
        dict[attribute] = [obj["score"]]
    else:
        dict[attribute].append(obj["score"])

def createGraph(dicty):
    data = []
    keys = []
    for key in dicty:
        keys.append(key)
        data.append(dicty[key])
    
    fig, ax = plt.subplots()
    
    plt.boxplot(data)
    ax.set_xticklabels(keys)
    plt.show()

for root, dirs, files in os.walk("ai-soc/test images"):
    for f in files:
        if f not in nsfwDict:
            temp = (os.path.relpath(os.path.join(root, f), "."))
            if ((".jpg" in temp) and (count < newImgsToCheck)):
                if ("CFD" in temp):
                    # request = makeRequest(temp)
                    # nsfwDict[f] = {
                    #     'database': "CFD",
                    #     'fullPath': temp,
                    #     'score': request,
                    #     'race': f[4],
                    #     'gender': f[5],
                    #     'modelId': f[7:10],
                    #     'imageId': f[11:14],
                    #     'expression': f[15:-4],
                    # }
                    pass
                elif ("UTKFace" in temp):
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
    
# for key in nsfwDict:
#     parseData(nsfwDict[key])

with open(outputFileName, 'w') as fp:
    json.dump(nsfwDict, fp, indent=4)

# createGraph(intersectionalDict)