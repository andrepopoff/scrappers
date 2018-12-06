"""This script parses the data from https://www.liveinternet.ru/rating/ru/"""
import requests
import csv
from multiprocessing import Pool


def get_html(url):
    response = requests.get(url)
    return response.text


def write_csv(data, fieldnames):
    with open('websites.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)


def get_page_data(text):
    fieldnames = 'name', 'url', 'description', 'traffic', 'percent'
    data = text.strip().split('\n')[1:]

    for row in data:
        name, url, description, traffic, percent, tail = row.strip().split('\t')
        data = dict(zip(fieldnames, (name, url, description, traffic, percent)))
        write_csv(data, fieldnames)


def make_all(url):
    text = get_html(url)
    get_page_data(text)


def main():
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'
    urls = [url.format(i) for i in range(1, 5000)]

    with Pool(20) as p:
        p.map(make_all, urls)


if __name__ == '__main__':
    main()