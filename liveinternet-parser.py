import requests
import csv


def get_html(url):
    response = requests.get(url)
    return response.text


def write_csv(data):
    with open('websites.csv', 'a') as f:
        order = []
        writer = csv.DictWriter(f, fieldnames=[])
        writer.writerow(data)
        

def main():
    pass


if __name__ == '__main__':
    main()