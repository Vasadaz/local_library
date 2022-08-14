import downloader

LIBRARY_PATH_DIR = 'books'

if __name__ == '__main__':
    url = 'https://tululu.org/txt.php?id=32168'
    downloader.download_file(url, LIBRARY_PATH_DIR)
