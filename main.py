import argparse
import requests
import time

from urllib.parse import urljoin

import downloader

IMAGE_DIR_NAME = 'covers'
LIBRARY_DIR_NAME = 'books'
LIBRARY_URL = 'https://tululu.org/'


def get_library_notes(book_id: int) -> dict:
    book_download_txt_url = urljoin(LIBRARY_URL, f'txt.php')
    book_download_txt_url_params = {'id': book_id}
    book_page_url = urljoin(LIBRARY_URL, f'b{book_id}/')

    response = requests.get(book_page_url)
    response.raise_for_status()

    downloader.check_for_redirect(response)

    library_notes = downloader.parse_library_notes(response, book_id)
    book_name = library_notes['book']
    library_notes['book_path'] = downloader.download_txt(
        book_download_txt_url,
        LIBRARY_DIR_NAME,
        book_name,
        book_download_txt_url_params
    )
    library_notes['cover_path'] = downloader.download_img(
        library_notes['cover_url'],
        IMAGE_DIR_NAME
    )
    del library_notes['cover_url']

    return library_notes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Скрипт скачивает книги по их id с онлайн-библиотеки https://tululu.org  '
                    '\nКниги сохраняются в директории ./books , а обложки к ним в ./covers '
    )
    parser.add_argument(
        '-s',
        '--start_id',
        help='Начало диапазона id, по-умолчанию 1',
        default=1,
        type=int
    )
    parser.add_argument(
        '-e',
        '--end_id',
        help='Конец диапазона id, по-умолчанию 10',
        default=10,
        type=int
    )
    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':
    args = parse_args()
    start_id = args.start_id
    end_id = args.end_id + 1

    for book_id in range(start_id, end_id):
        while True:
            try:
                book_notes = get_library_notes(book_id)

                print(f'Book №{book_id}:')
                for category, note in book_notes.items():
                    print(f'{category} - {note}')
                print()

                break
            except requests.exceptions.HTTPError as err:
                print(f'Book №{book_id} Not Found {err.args[0]}\n')
                break
            except requests.exceptions.ConnectionError as err:
                print(f'Connection Error: Book №{book_id}\n{err}\n')
                time.sleep(5)
                continue
