import downloader
import requests


LIBRARY_PATH_DIR = 'books'


if __name__ == '__main__':
    for book_id in range(1, 11):
        params = {'id': book_id}
        download_url = 'https://tululu.org/txt.php'
        page_url = f'https://tululu.org/b{book_id}'

        try:
            save_path = downloader.download_file(LIBRARY_PATH_DIR, download_url, params)
            book_notes = downloader.parser_book_name(page_url)
        except requests.exceptions.HTTPError:
            print(f'Book №{book_id} Not Found')
            continue

        print(f'Save book №{book_id} to {save_path}')
        print(book_notes)
