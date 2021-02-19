import requests
r = requests.post(
    "https://api.deepai.org/api/nsfw-detector",
    files={
        'image': open('./test images/Screenshot_200.png', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())