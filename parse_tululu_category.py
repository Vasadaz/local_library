import argparse
import json
import os
import time

from pathlib import Path
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup

import downloader


IMAGE_DIR_NAME = 'covers'
LIBRARY_DIR_NAME = 'books'
LIBRARY_URL = 'https://tululu.org/'

def get_last_page_num(response) -> int:
    soup = BeautifulSoup(response.text, 'lxml')
    selectors = '#content a.npage'
    last_page_num_tag = soup.select(selectors)[-1]
    last_page_num = int(last_page_num_tag.text)

    return last_page_num


def get_book_resources(book_id: int,
                       get_cover: bool = True,
                       get_txt: bool = True,
                       ) -> dict:
    global IMAGE_DIR_NAME, LIBRARY_DIR_NAME, LIBRARY_URL

    book_download_txt_url = urljoin(LIBRARY_URL, f'txt.php')
    book_download_txt_url_params = {'id': book_id}
    book_page_url = urljoin(LIBRARY_URL, f'b{book_id}/')

    response = requests.get(book_page_url)
    response.raise_for_status()

    downloader.check_for_redirect(response)

    library_notes = downloader.parse_library_notes(response, book_id)
    book_name = library_notes['book']

    if get_txt:
        library_notes['book_path'] = downloader.download_txt(
            book_download_txt_url,
            LIBRARY_DIR_NAME,
            book_name,
            book_download_txt_url_params
        )
    if get_cover:
        library_notes['cover_path'] = downloader.download_img(
            library_notes['cover_url'],
            IMAGE_DIR_NAME
        )
    del library_notes['cover_url']

    return library_notes


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
        type=int,
    )
    parser.add_argument(
        '-e',
        '--end_page',
        help='Конец диапазона страниц, по-умолчанию 4',
        type=int,
    )
    parser.add_argument(
        '--dest_folder',
        help='Указание пути к каталогу с результатами парсинга: картинкам, книгам, JSON.',
        type=str,
    )
    parser.add_argument(
        '--skip_imgs',
        help='Скрипт не будет скачивать картинки',
        action='store_true',
    )
    parser.add_argument(
        '--skip_txt',
        help='Скрипт не будет скачивать книги',
        action='store_true',
    )
    parser.add_argument(
        '--json_path',
        help='Указание пути к JSON файлу с результатами.',
        type=str,
        default='./library_books.json'
    )
    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':
    category_url = 'https://tululu.org/l55/'

    args = parse_args()
    start_page = args.start_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_path = args.json_path

    if args.end_page:
        end_page = args.end_page + 1
    else:
        response = requests.get(category_url)
        response.raise_for_status()
        end_page = get_last_page_num(response) + 1

    if dest_folder:
        Path(dest_folder).mkdir(parents=True, exist_ok=True)
        IMAGE_DIR_NAME = os.path.join(dest_folder, IMAGE_DIR_NAME)
        LIBRARY_DIR_NAME = os.path.join(dest_folder, LIBRARY_DIR_NAME)

    category_book_tags = []
    library_books = {}

    for page_num in range(start_page, end_page):
        page_num_url = urljoin(category_url, str(page_num))

        response = requests.get(page_num_url)
        response.raise_for_status()

        book_tags = parse_book_tags(response)
        category_book_tags.extend(book_tags)

    for tag in category_book_tags:
        while True:
            book_id = tag['href'].strip('/b')

            try:
                book_notes = get_book_resources(book_id)
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

    with open(json_path, 'w+', encoding='utf8') as file:
        file.write(library_json)
