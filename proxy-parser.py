import requests
from bs4 import BeautifulSoup


def get_html(url):
    # proxies = {'https': 'ipaddress:5000'}
    response = requests.get(url)
    return response.text


def get_proxy(html):
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


def main():
    url = 'https://free-proxy-list.net/'
    get_proxy(get_html(url))


if __name__ == '__main__':
    main()