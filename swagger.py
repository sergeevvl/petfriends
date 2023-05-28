import requests
import json

baseurl = "https://petstore.swagger.io/v2/"

res = requests.get(f"{baseurl}pet/findByStatus?", params={'status': 'available'}, headers={'accept': 'application/json'})

print(res.text)

res = requests.post(f"{baseurl}pet", headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                    data={'id': 0,
                          'category': {'id': 0, 'name': 'newpetname'},
                          'name': 'песель',
                          'photoUrls': ["string"],
                          'tags': [{'id': 0, 'name': 'собачки'}],
                          'status': 'available'})

print(res.text)
