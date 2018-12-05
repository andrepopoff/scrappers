"""Coinmarketcap.com site parsing."""
import requests
import csv
import re

from bs4 import BeautifulSoup
from peewee import PostgresqlDatabase, CharField, TextField, Model


db = PostgresqlDatabase(database='coins', user='postgres', password='Lub08mpostgresql', host='localhost')


class Coin(Model):
    name = CharField()
    symbol = CharField()
    url = TextField()
    price = CharField()

    class Meta:
        database = db


def get_html(url):
    """Returns the HTML code of the page."""
    response = requests.get(url)
    if response.ok:
        return response.text
    print('Error', response.status_code)


def write_csv(to_file, data, fieldnames):
    """Writes data in csv file."""
    with open(to_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data[name] for name in fieldnames))


def get_page_data(html, page, to_file, fieldnames):
    """Gets data from https://coinmarketcap.com/"""
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='currencies').find('tbody').find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')

        try:
            name = tds[1].find('a', class_='currency-name-container').text.strip()
        except:
            name = ''

        try:
            symbol = tds[1].find('a').text.strip()
        except:
            symbol = ''

        try:
            url = page[:-1] + tds[1].find('a').get('href')
        except:
            url = ''

        try:
            price = tds[3].find('a').get('data-usd')
        except:
            price = ''

        data = dict(zip(fieldnames, (name, symbol, url, price)))

        write_csv(to_file, data, fieldnames)


def save_in_db(from_file, fieldnames):
    """Saves data in database"""
    db.connect()
    db.create_tables([Coin])

    with open(from_file) as file:
        reader = csv.DictReader(file, fieldnames=fieldnames)
        coins = list(reader)

        with db.atomic():
            for i in range(0, len(coins), 100):
                Coin.insert_many(coins[i:i+100]).execute()


def main():
    base_url = 'https://coinmarketcap.com/'
    filename = 'cmc.csv'
    fieldnames = 'name', 'symbol', 'url', 'price'
    url = base_url

    while True:
        get_page_data(get_html(url), url, filename, fieldnames)
        soup = BeautifulSoup(get_html(url), 'lxml')

        try:
            pattern = 'Next'
            url = base_url + soup.find('ul', class_='pagination').find('a', text=re.compile(pattern)).get('href')
        except:
            break

    save_in_db(filename, fieldnames)


if __name__ == '__main__':
    main()
