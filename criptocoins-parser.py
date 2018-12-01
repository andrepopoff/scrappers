"""Coinmarketcap.com site parsing."""
import requests
import csv

from bs4 import BeautifulSoup


def get_html(url):
    """Returns the HTML code of the page."""
    response = requests.get(url)
    if response.ok:
        return response.text
    print('Error', response.status_code)


def write_csv(data):
    """Writes data in csv file."""
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['symbol'], data['url'], data['price']))


def get_page_data(html, page):
    """Gets data from https://coinmarketcap.com/"""
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='currencies').find('tbody').find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        name = tds[1].find('a', class_='currency-name-container').text
        symbol = tds[1].find('a').text
        url = page[:-1] + tds[1].find('a').get('href')
        price = tds[3].find('a').get('data-usd')

        data = {
            'name': name,
            'symbol': symbol,
            'url': url,
            'price': price
        }

        write_csv(data)


def main():
    url = 'https://coinmarketcap.com/'
    get_page_data(get_html(url), url)


if __name__ == '__main__':
    main()
