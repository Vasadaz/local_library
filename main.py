import downloader


LIBRARY_PATH_DIR = 'books'


if __name__ == '__main__':
    for book_id in range(1, 11):
        params = {'id': book_id}
        url = 'https://tululu.org/txt.php'
        save_path = downloader.download_file(LIBRARY_PATH_DIR, url, params)
        print(save_path)
