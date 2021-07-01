import requests
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout
my_proxies = {
    'http': 'http://46.138.246.248:8088',
    'https': 'http://46.138.246.248:8088',
}
try:
    response = requests.get('http://httpbin.org/ip', proxies=my_proxies, timeout=6)
except:
    print("Unable to connect to the proxy.")
else:
    print(response.json())
