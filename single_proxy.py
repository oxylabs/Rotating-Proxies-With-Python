import requests
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout

PROXY = 'http://194.163.131.117:8080'
TIMEOUT_IN_SECONDS = 10

scheme_proxy_map = {
    'http': PROXY,
}
try:
    response = requests.get('http://httpbin.org/ip', proxies=scheme_proxy_map, timeout=TIMEOUT_IN_SECONDS)
except (ProxyError, ReadTimeout, ConnectTimeout) as error:
    print(f'Unable to connect to the proxy: #{error}')
else:
    print(response.json())
