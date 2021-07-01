import csv
import requests
MAX_TRY = 5


def get_next_proxy(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            yield row[0]


def main():
    good = 0
    for proxy in get_next_proxy('proxies.csv'):
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
        except:
            pass
        else:
            print(response.json())
            good += 1

    print('Good proxies --->', good)


if __name__ == '__main__':
    main()
