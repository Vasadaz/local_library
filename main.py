import requests

import downloader

IMAGE_DIR_NAME = 'covers'
LIBRARY_DIR_NAME = 'books'
LIBRARY_URL = 'https://tululu.org/'

if __name__ == '__main__':
    for book_id in range(1, 11):
        try:
            book_resources = downloader.parse_book_page(LIBRARY_URL, book_id)
            book_name = book_resources['book']
            book_url = book_resources['txt_url']
            cover_url = book_resources['cover_url']
            book_resources['book_path'] = downloader.download_txt(book_url, LIBRARY_DIR_NAME, book_name)
            book_resources['cover_path'] = downloader.download_img(cover_url, IMAGE_DIR_NAME)
        except requests.exceptions.HTTPError:
            print(f'Book №{book_id} Not Found\n')
            continue

        for note in book_resources.items():
            print(note)
        print()
