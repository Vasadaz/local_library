import requests

import downloader


IMAGE_DIR_NAME = 'covers'
LIBRARY_PATH_DIR = 'books'
LIBRARY_URL = 'https://tululu.org/'


if __name__ == '__main__':
    for book_id in range(1, 11):
        params = {'id': book_id}
        download_url = f'{LIBRARY_URL}txt.php'
        page_url = f'{LIBRARY_URL}b{book_id}'

        try:
            book_resources = downloader.download_txt_file(LIBRARY_PATH_DIR, LIBRARY_URL, params)
            image_url = book_resources['image_url']
            book_resources['image_path'] = downloader.download_img(IMAGE_DIR_NAME, image_url)
        except requests.exceptions.HTTPError:
            print(f'Book №{book_id} Not Found\n')
            continue
        for note in book_resources.items():
            print(note)
        print()
