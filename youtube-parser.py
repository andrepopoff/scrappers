"""
This script parses the name of the video and links to the video from the youtube channel and writes data in csv file
"""

import requests
import sys
import csv

from bs4 import BeautifulSoup


BASE_URL = 'https://www.youtube.com'


def get_response(url):
    response = requests.get(url)
    return response


def get_html(response, json_header):
    if 'html' in response.headers['Content-Type']:
        return response.text
    elif 'json' in response.headers['Content-Type']:
        return response.json()[json_header]
    else:
        print('Unknown server response type')
        sys.exit(0)


def write_csv(data):
    with open('videos.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'url'])
        writer.writerow(data)


def get_page_data(response):
    html = get_html(response, 'content_html')
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('h3', class_='yt-lockup-title')

    for item in items:
        name = item.text.strip()
        url = item.find('a').get('href')
        data = {'name': name, 'url': BASE_URL + url}
        write_csv(data)


def get_next_url(response):
    html = get_html(response, 'load_more_widget_html')
    soup = BeautifulSoup(html, 'lxml')

    try:
        url = BASE_URL + soup.find('button', class_='load-more-button').get('data-uix-load-more-href')
    except:
        url = ''

    return url


def main():
    url = BASE_URL + '/user/schafer5/videos?gl=RU'

    while url:
        response = get_response(url)
        get_page_data(response)
        url = get_next_url(response)


if __name__ == '__main__':
    main()