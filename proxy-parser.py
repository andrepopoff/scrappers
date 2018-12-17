import requests

from bs4 import BeautifulSoup
from random import choice


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:11]
    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)

    return choice(proxies)


def get_html(url):
    proxies_params = get_proxy()
    proxy = {proxies_params['schema']: proxies_params['address']}
    response = requests.get(url, proxies=proxy, timeout=5)
    return response.json()['origin']


def main():
    get_html('http://httpbin.org/ip')


if __name__ == '__main__':
    main()