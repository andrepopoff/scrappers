import requests
import csv


def get_html(url):
    response = requests.get(url)
    return response.text


def write_csv(data):
    with open('websites.csv', 'a') as f:
        order = ['name', 'url', 'description', 'traffic', 'percent']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def main():
    for i in range(1, 7945):
        url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'.format(i)
        response = get_html(url)
        data = response.strip().split('\n')[1:]

        for row in data:
            columns = row.strip().split('\t')
            name = columns[0]
            url = columns[1]
            description = columns[2]
            traffic = columns[3]
            percent = columns[4]

            data = {
                'name': name,
                'url': url,
                'description': description,
                'traffic': traffic,
                'percent': percent
            }

            write_csv(data)


if __name__ == '__main__':
    main()