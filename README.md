# Rotating Proxies With Python
[<img src="https://img.shields.io/static/v1?label=&message=Python&color=brightgreen" />](https://github.com/topics/python) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping) [<img src="https://img.shields.io/static/v1?label=&message=Rotating%20Proxies&color=blueviolet" />](https://github.com/topics/rotating-proxies)

## Table of Contents

- [Finding Current IP Address](#finding-current-ip-address)
- [Using Single Proxy](#using-single-proxy)
- [Rotating Multiple Proxies](#rotating-multiple-proxies)
- [Retrying With Next Proxy](#retrying-with-next-proxy)

Whenever a webpage is requested using a browser or code, the request reaches the web server, and the web server returns a response.

In this case, the web server knows everything about the client. The most important information here is the IP address. This may not be desired for several reasons. For example, one such case is privacy concerns. Another use case is web scraping at scale - if a server receives a lot of requests from the same IP, the web server can throttle or slow down the speed of returning the response. The web server can also completely ban that IP address, either temporarily or permanently.

The solution to this problem is using a lot of proxies. With multiple proxies, a rotation of the servers can be put in place. That means that effectively every request will be reaching the web server from a different IP. This article covers this specific scenario. We will build a web scraper from the ground up and move on to create a solution that implements rotation of proxies using Python.

## Finding Current IP Address

Before we explore various ways to rotate proxies with Python, we need to standardize the code used to get the current IP address. 

A very useful site for this kind of testing is [httpbin.org](http://httpbin.org/). This website exposes many helpful methods. For our use, the most useful one is [http://httpbin.org/ip](http://httpbin.org/ip). This simply returns a JSON object that contains the IP address.

This article uses the Requests module. If you do not have it installed, install it from a terminal by running the following command:

```sh
$pip install requets
```

If you get permission errors, either use a virtual environment or add `--user` switch the pip command.

Write the following code in a `.py` file, or use the [no_proxy.py](code/no_proxy.py) and run it from a terminal.

```python
import requests

response = requests.get('http://httpbin.org/ip')
print(response.json())
```

The output of this script will show the current IP address.

```sh
$python no_proxy.py
{'origin': '128.90.50.100'}
```

Take a note of this proxy. This is the real proxy address. We will modify this code and ensure that this IP address changes.

Let's start with a single proxy.

## Using Single Proxy 

**Important Note**: Free proxies are usually slower and unreliable. It is highly recommended to use reliable proxies. 

For this example, we are going to use a proxy with IP 46.138.246.248 and port 8088. 

The Requests module can handle proxies directly. The proxies need to be supplied to the `requests.get` function as a dictionary. This dictionary contains two keys—`http` and `https`. Each key's value is the proxy address, which should include the protocol, IP address, and, if applicable, user name and password for authentication. You can refer to the official [documentation here](https://docs.python-requests.org/en/master/user/advanced/#proxies). 

The following is a simple example of the proxies dictionary:

```python
my_proxies = {
    'http': 'http://46.138.246.248:8088',
    'https': 'http://46.138.246.248:8088'
}
```

Note that if the proxies require authentication, the user name and the password can be included in the proxies as follows:

```python
proxies_with_auth = {
    'http': 'http://username:password@46.138.246.248:8088',
    'https': 'http://username:password@46.138.246.248:8088'
}
```

Once this dictionary is created, this can be supplied to the get method as a value for the parameter `proxies`.

```python
response = requests.get('http://httpbin.org/ip', proxies=my_proxies)
```

**Important Notes:**

- These free proxies are usually very slow. Instead of waiting for a long time, it may be a good idea to set the `timeout` parameter explicitly.
- If the proxy cannot be connected, one of these exceptions can be raised - `ProxyError`, `ReadTimeout`, `ConnectTimeout`. 

It will be a good idea to use a `try - except - else` block. The `else` block is executed only if no exception is thrown. Further, these exceptions can be explicitly written, or we can take a shortcut and omit the exception type. Note that catching all exceptions directly is not considered to be a good practice.

```python
try:
    response = requests.get('http://httpbin.org/ip', proxies=my_proxies, timeout=5)
except:
    print("Unable to connect to the proxy.")
else: # executes only if no excepton
    print(response.json())	
```

The output of this script is as follows:

```sh
$python single_proxy.py
{'origin': '46.138.246.248'}
```

As it is evident here, the IP address reflected here is that of the proxy. You can find the complete code in the file [single_proxy.py](code/single_proxy.py).

## Rotating Multiple Proxies

If multiple proxies are available, it is possible to rotate proxies with Python. Some websites allow downloading a list of proxies as CSV or similar format. This list can be used to implement proxy rotation.

In this example, we will be working with a file downloaded from one of the free websites. This file contains the proxies in this format:

```
5.235.187.58:999
46.138.246.248:8088
103.9.191.174:56765
43.231.21.176:36415
68.183.221.156:41933
..
```

To get a rotating IP proxy using this file, first, we need to write a function that can return one proxy at a time. This is a crucial step to implement proxy rotation. It can be achieved by using a generator function. These functions use the `yield` keyword instead of the usual `return` keyword and they keep track of the last value returned. This means that in the next call, a different value can be returned.

This function will return the first row every time it is called. If the return statement is replaced with a yield statement, it will process one row every time it is executed.

```python
        ...
    	for row in reader:
            yield row[0] # Returns next row with each call
```

This function is the most important part of this proxy-rotator script. It is responsible for sending one proxy at a time. To implement proxy rotation, this function can be called in a loop to get the proxies one by one. Here is one example:

```python
for proxy in get_next_proxy('proxies.csv'):
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
    except:
        print(f'{proxy} - not working')
    else:
        print(response.json(), '- WORKING ')
```

This complete code is available in [rotating_multiple_proxies.py](code/rotating_multiple_proxies.py)

## Retrying With Next Proxy

The previous section explained how to rotate proxies with Python. This proxy-rotator can be improved to incorporate real word usage. For example, typically, a request has to be processed using a proxy. If that particular proxy is not working, then the code must try the same request with the next available proxy.

To achieve this, a `while True` loop can be used with carefully controlled `break`s. 

**Warning**: `while True` loop can end up running forever even if a small bug creeps in. It is always a good idea to have a backup `break`, based on a counter. For example, no matter the outcome, the break must end after 1000 iterations.

To create this proxy-rotator,  we are going to reuse the `get_next_proxy()` function created in the previous section. In this section, we will create another function. 

Before even beginning the loop, it is important to call the `get_next_proxy()` function and store the generator returned.

```python
proxy_gen = get_next_proxy('proxies.csv')
```
After we have stored the instance of the generator, we will write the while True loop:

```python
while True:
    # rest of the code
```

To get the first proxy for this proxy rotator, we will use the next operator of Python, which gets the next item from the generator object.

```python
proxy=next(proxy_gen)
```

Once we have the proxy, we will send the get request. In case of an exception, we will `continue` the loop. If there are no errors, we will stop further iterations of the loop by calling `break`.

```python
while True:
    proxy=next(proxy_gen)
    proxies = {
            'http': proxy,
            'https': proxy,
        }
     try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=1)
     except:
		continue # try with next proxy
     else:
         print(response.json()) #process response
         break # Terminate the loop
```

The `next` operator raises the `StopIteration` exception when the list is exhausted. You can use a try-except block to handle this error and terminate the loop gracefully.

```python
try:
	proxy = next(proxy_gen)
except StopIteration:
	print('proxy list exausted')
	break  # proxy list exausted
```

For the complete code, please see [retrying_next.py](code/retrying_next.py). 

These scripts can be modified as per your specific requirements.
