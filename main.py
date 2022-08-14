import downloader
import requests


LIBRARY_PATH_DIR = 'books'


if __name__ == '__main__':
    for book_id in range(1, 11):
        params = {'id': book_id}
        url = 'https://tululu.org/txt.php'

        try:
            save_path = downloader.download_file(LIBRARY_PATH_DIR, url, params)
        except requests.exceptions.HTTPError:
            print(f'Book №{book_id} Not Found')
            continue

        print(f'Save book №{book_id} to {save_path}')
