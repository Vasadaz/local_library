import argparse
import json
import time
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup

from main import get_library_notes


def get_last_page_num(response) -> int:
    soup = BeautifulSoup(response.text, 'lxml')
    selectors = '#content a.npage'
    last_page_num_tag = soup.select(selectors)[-1]
    last_page_num = int(last_page_num_tag.text)

    return last_page_num


def parse_book_tags(response) -> list:
    soup = BeautifulSoup(response.text, 'lxml')
    selectors = '#content .bookimage a[href^="/b"]'
    content_urls = soup.select(selectors)

    return content_urls


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Скрипт для скачивания 25 книг с каждой страницы.'
                    '\nКниги сохраняются в директории ./books , а обложки к ним в ./covers '
    )
    parser.add_argument(
        '-s',
        '--start_page',
        help='Начало диапазона страниц, по-умолчанию 1',
        default=1,
        type=int
    )
    parser.add_argument(
        '-e',
        '--end_page',
        help='Конец диапазона страниц, по-умолчанию 4',
        default=5,
        type=int
    )
    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':
    category_url = 'https://tululu.org/l55/'

    args = parse_args()
    start_page = args.start_page

    if args.end_page > start_page:
        end_page = args.end_page + 1
    else:
        response = requests.get(category_url)
        response.raise_for_status()
        end_page = get_last_page_num(response) + 1

    category_book_tags = []
    library_books = {}

    for page_num in range(start_page, end_page):
        print(page_num)
        page_num_url = urljoin(category_url, str(page_num))
        response = requests.get(page_num_url)
        response.raise_for_status()
        get_last_page_num(response)
        book_tags = parse_book_tags(response)
        category_book_tags.extend(book_tags)

    for tag in category_book_tags:
        while True:
            book_id = tag['href'].strip('/b')

            try:
                book_notes = get_library_notes(book_id)
                library_books[book_id] = book_notes
                break
            except requests.exceptions.HTTPError as err:
                book_url = urljoin(err.args[0], f'b{book_id}')
                print(f'Book №{book_id} Not Found {book_url}\n')
                break
            except requests.exceptions.ConnectionError as err:
                print(f'Connection Error: Book №{book_id}\n{err}\n')
                time.sleep(5)
                continue

    library_json = json.dumps(library_books)

    with open("library_books.json", "w+", encoding='utf8') as file:
        file.write(library_json)
