import csv
import requests


def get_next_proxy(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            yield row[0]


def main():
    proxy_gen = get_next_proxy('proxies.csv')
    while True:
        try:
            proxy = next(proxy_gen)
        except StopIteration:
            print('proxy list exausted')
            break  # proxy list exausted
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
        except:
            continue
        else:
            print(response.json())
            break


if __name__ == '__main__':
    main()
