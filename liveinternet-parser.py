"""This script parses the data from https://www.liveinternet.ru/rating/ru/"""
import requests
import csv


def get_html(url):
    response = requests.get(url)
    return response.text


def write_csv(data, fieldnames):
    with open('websites.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)


def main():
    fieldnames = 'name', 'url', 'description', 'traffic', 'percent'

    for i in range(1, 8997):
        url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'.format(i)
        response = get_html(url)
        data = response.strip().split('\n')[1:]

        for row in data:
            name, url, description, traffic, percent, tail = row.strip().split('\t')
            data = dict(zip(fieldnames, (name, url, description, traffic, percent)))
            write_csv(data, fieldnames)


if __name__ == '__main__':
    main()