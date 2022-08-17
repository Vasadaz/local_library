import argparse
import requests

import downloader

IMAGE_DIR_NAME = 'covers'
LIBRARY_DIR_NAME = 'books'
LIBRARY_URL = 'https://tululu.org/'


def parse_arg() -> argparse.Namespace:
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
    args = parse_arg()
    start_id = args.start_id
    end_id = args.end_id + 1

    for book_id in range(start_id, end_id):
        try:
            book_resources = downloader.parse_book_page(LIBRARY_URL, book_id)
            book_name = book_resources['book']
            book_url = book_resources['txt_url']
            cover_url = book_resources['cover_url']
            book_resources['book_path'] = downloader.download_txt(book_url, LIBRARY_DIR_NAME, book_name)
            book_resources['cover_path'] = downloader.download_img(cover_url, IMAGE_DIR_NAME)
        except requests.exceptions.HTTPError as err:
            print(f'Book №{book_id} Not Found {err.args[0]}\n')
            continue

        print(f'Book №{book_id}:')
        for note in book_resources.items():
            print(f'{note[0]} - {note[1]}')
        print()
