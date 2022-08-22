import time
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup

from main import get_library_notes

import pprint


def parse_book_tags(response) -> list:
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find(id='content')
    content_urls = content.find_all('div', class_="bookimage")

    return content_urls


if __name__ == '__main__':
    category_url = 'https://tululu.org/l55/'
    category_book_tags = []
    library_books = {}

    for page_num in range(1, 3):
        page_num_url = urljoin(category_url, str(page_num))
        response = requests.get(page_num_url)
        response.raise_for_status()
        book_tags = parse_book_tags(response)
        category_book_tags.extend(book_tags)

    for tag in category_book_tags:
        while True:
            book_id = tag.find('a')['href'].strip('/b')

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

