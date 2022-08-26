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
JSON_FILE_NAME = 'library_books.json'


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


def get_book_tags(page_num: int) -> list:
    page_num_url = urljoin(category_url, str(page_num))
    response = requests.get(page_num_url)
    response.raise_for_status()
    book_tags = parse_book_tags(response)

    return book_tags


def get_last_page_num(page_url) -> int:
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selectors = '#content a.npage'
    last_page_num_tag = soup.select(selectors)[-1]
    last_page_num = int(last_page_num_tag.text)

    return last_page_num


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Скрипт для скачивания книг из указанной категории онлайн-библиотеки https://tululu.org .'
                    '\nКниги сохраняются в директорию ./books , а обложки к ним в ./covers .' 
                    '\nВся информация по книгам сохраняется в JSON файл - library_books.json .'
    )
    parser.add_argument(
        '-c',
        '--category_url',
        help='Ссылка на категорию, по умолчанию  категория "Научная фантастика" https://tululu.org/l55/',
        default='https://tululu.org/l55/'
    )
    parser.add_argument(
        '-s',
        '--start_page',
        help='Начало диапазона страниц, по-умолчанию 1',
        type=int,
        default=1
    )
    parser.add_argument(
        '-e',
        '--end_page',
        help='Конец диапазона страниц, по-умолчанию последняя страница',
        type=int,
    )
    parser.add_argument(
        '--dest_folder',
        help='Указание пути к каталогу с результатами парсинга: картинкам, книгам, JSON.',
    )
    parser.add_argument(
        '--skip_imgs',
        help='Скрипт не будет скачивать картинки',
        action='store_false',
    )
    parser.add_argument(
        '--skip_txt',
        help='Скрипт не будет скачивать книги',
        action='store_false',
    )
    parser.add_argument(
        '--json_path',
        help='Указание пути к JSON файлу с информацией по книгам.'
             '\nЕсли указан --dest_folder, то итоговый путь JSON файла:'
             '\nDEST_FOLDER/JSON_PATH/library_books.json',
    )
    parsed_args = parser.parse_args()

    return parsed_args


def parse_book_tags(response) -> list:
    soup = BeautifulSoup(response.text, 'lxml')
    selectors = '#content .bookimage a[href^="/b"]'
    content_urls = soup.select(selectors)

    return content_urls


def prevent_network_errors(function, **kwargs):
    while True:
        try:
            function_return = function(**kwargs)
            return function_return
        except requests.exceptions.HTTPError:
            print(f'Resource Not Found: function {function.__name__}({kwargs})')
            return
        except requests.exceptions.ConnectionError:
            print(f'Connection Error: function {function.__name__}({kwargs})')
            time.sleep(5)
            continue


if __name__ == '__main__':
    args = parse_args()
    category_url = args.category_url
    start_page = args.start_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_path = args.json_path

    if args.end_page:
        end_page = args.end_page + 1
    else:
        end_page = prevent_network_errors(get_last_page_num, page_url=category_url) + 1

    if dest_folder:
        Path(dest_folder).mkdir(parents=True, exist_ok=True)
        IMAGE_DIR_NAME = os.path.join(dest_folder, IMAGE_DIR_NAME)
        LIBRARY_DIR_NAME = os.path.join(dest_folder, LIBRARY_DIR_NAME)
        json_path = os.path.join(dest_folder, json_path)

    if json_path:
        Path(json_path).mkdir(parents=True, exist_ok=True)
        json_full_file_name = os.path.join(json_path, JSON_FILE_NAME)
    else:
        json_full_file_name = JSON_FILE_NAME

    category_book_tags = []
    library_books = {}

    for page_num in range(start_page, end_page):
        book_tags = prevent_network_errors(get_book_tags, page_num=page_num)
        category_book_tags.extend(book_tags)

    for tag in category_book_tags:
        book_id = tag['href'].strip('/b')
        book_notes = prevent_network_errors(
            get_book_resources,
            book_id=book_id,
            get_cover=skip_imgs,
            get_txt=skip_txt,
        )
        library_books[book_id] = book_notes

    library_json = json.dumps(library_books)

    with open(json_full_file_name, 'w+', encoding='utf8') as file:
        file.write(library_json)
