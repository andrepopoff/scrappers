import requests
import sys
import csv

from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response


def write_csv(data):
    with open('videos.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'url'])
        writer.writerow(data)


def get_page_data(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    elif 'json' in response.headers['Content-Type']:
        html = response.json()['content_html']
    else:
        print('Unknown server response type')
        sys.exit(0)

    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('h3', class_='yt-lockup-title')

    for item in items:
        name = item.text.strip()
        url = item.find('a').get('href')
        data = {'name': name, 'url': url}
        write_csv(data)


def main():
    # url = 'https://www.youtube.com/browse_ajax?ctoken=4qmFsgJAEhhVQ0NleklnQzk3UHZVdVI0X2diRlVzNWcaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk5yZ0JBQSUzRCUzRA%253D%253D&continuation=4qmFsgJAEhhVQ0NleklnQzk3UHZVdVI0X2diRlVzNWcaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk5yZ0JBQSUzRCUzRA%253D%253D&itct=CBwQybcCIhMI8o37o9aV3wIVw5RVCh1E9AsI'
    # url = 'https://www.youtube.com/browse_ajax?ctoken=4qmFsgJAEhhVQ0NleklnQzk3UHZVdVI0X2diRlVzNWcaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk5iZ0JBQSUzRCUzRA%253D%253D&continuation=4qmFsgJAEhhVQ0NleklnQzk3UHZVdVI0X2diRlVzNWcaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk5iZ0JBQSUzRCUzRA%253D%253D&itct=CBwQybcCIhMIobnTodaV3wIVg7xVCh3MOQNp'

    url = 'https://www.youtube.com/user/schafer5/videos?gl=RU'
    # url1 = 'https://www.youtube.com/browse_ajax?action_continuation=1&amp;continuation=4qmFsgJAEhhVQ0NleklnQzk3UHZVdVI0X2diRlVzNWcaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk1yZ0JBQSUzRCUzRA%253D%253D;&amp;direct_render=1'
    url2 = 'https://www.youtube.com/browse_ajax?action_continuation=1&amp;continuation=4qmFsgJAEhhVQ0NleklnQzk3UHZVdVI0X2diRlVzNWcaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk03Z0JBQSUzRCUzRA%253D%253D'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()