import os.path
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def parse_urls(response) -> list:
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find(id='content')
    content_urls = content.find_all('div', class_="bookimage")
    return content_urls


if __name__ == '__main__':
    category_url = 'https://tululu.org/l55/'
    category_urls = []
    book_urls = []

    for page_num in range(1, 101):
        page_num_url = urljoin(category_url, str(page_num))
        response = requests.get(page_num_url)
        response.raise_for_status()
        # category_urls.extend(parse_urls(response))
        print(response.url)
        for url in parse_urls(response):
            book_url = urljoin(response.url, url.find('a')['href'])
            book_urls.append(book_url)
            print('\t', book_url)
        print()
        print(len(book_urls))