import requests

response = requests.get('http://httpbin.org/ip')
print(response.json())
