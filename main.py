import requests
from bs4 import BeautifulSoup


def get_html(url):
    """Returns the HTML code of the page."""
    response = requests.get(url)
    return response.text


def get_data(html):
    """Returns the text in the <h1> tag for the wordpress.org"""
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', id='home-welcome').find('header').find('h1').text
    return h1


def main():
    url = 'https://wordpress.org'
    print(get_data(get_html(url)))


if __name__ == '__main__':
    main()
