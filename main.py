"""Wordpress.org site parsing."""
import requests
import csv

from bs4 import BeautifulSoup


def get_html(url):
    """Returns the HTML code of the page."""
    response = requests.get(url)
    return response.text


def get_h1(html):
    """Returns the text in the <h1> tag for the wordpress.org"""
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', id='home-welcome').find('header').find('h1').text
    return h1


def refined(string):
    """Example: 1,404 total ratings --> 1404"""
    r = string.split()[0]
    return r.replace(',', '')


def write_csv(data):
    """Writes data in csv file."""
    with open('plugins.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['url'], data['reviews']))


def get_data_from_popular_plugins(html):
    """Returns the data from Popular Plugins for the wordpress.org/plugins/"""
    soup = BeautifulSoup(html, 'lxml')
    popular = soup.find_all('section')[1]
    plugins = popular.find_all('article')

    for plugin in plugins:
        name = plugin.find('h2').text
        url = plugin.find('h2').find('a').get('href')

        r = plugin.find('span', class_='rating-count').find('a').text
        rating = refined(r)

        data = {
            'name': name,
            'url': url,
            'reviews': rating
        }

        write_csv(data)


def main():
    url = 'https://wordpress.org'
    print(get_h1(get_html(url)))

    url2 = url + '/plugins/'
    get_data_from_popular_plugins(get_html(url2))


if __name__ == '__main__':
    main()
