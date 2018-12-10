import requests


def get_html(url):
    response = requests.get(url)
    return response.text


def main():
    url = 'https://www.youtube.com/user/schafer5/videos'
    print(get_html(url))


if __name__ == '__main__':
    main()