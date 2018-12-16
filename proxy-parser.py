import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def get_proxy(html):
    soup = BeautifulSoup(html, 'lxml')
    pass

def main():
    pass


if __name__ == '__main__':
    main()