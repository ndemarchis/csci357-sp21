import requests
import os

import numpy as np
import matplotlib.pyplot as plt

count = 0
nsfwDict = {}
x = []
y = []

def makeRequest(path):
    print(path)
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            'image': open(path, 'rb'),
        },
        # headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        headers={'api-key': 'a35e4cbf-3de7-420a-8eee-16f3bbd24284'}
    )
    return (r.json()["output"]["nsfw_score"])

def addToArray(obj):
    x.append(int(obj["imageId"]))
    y.append(float(obj["score"]))

for root, dirs, files in os.walk("ai-soc/test images"):
    for f in files:
        temp = (os.path.relpath(os.path.join(root, f), "."))
        if ((".jpg" in temp) and (count < 2)):
            request = makeRequest(temp)
            nsfwDict[f] = {
                'fullPath': temp,
                'score': request,
                'race': f[4],
                'gender': f[5],
                'modelId': f[7:10],
                'imageId': f[11:14],
                'expression': f[15:-4],
            }
            addToArray(nsfwDict[f])
            count += 1
    
print(nsfwDict)
print(x)
print(y)

dt = 0.01
t = np.arange(0, 30, dt)

# plt.scatter(x, y, marker='o');
# plt.show()
# print(makeRequest('ai-soc/test images/CFD/AF-200/CFD-AF-200-228-N.jpg'))