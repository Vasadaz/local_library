import os.path
from pathlib import Path
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    http_code = {200: 'OK'}

    if response.status_code not in http_code:
        raise requests.HTTPError(response.url, response)


def download_txt_file(dir_name: str, url: str, params: dict = None) -> list:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    type_file = 'txt'
    download_url = urljoin(url, type_file + '.php')

    response = requests.get(download_url, params=params, allow_redirects=False)
    response.raise_for_status()

    check_for_redirect(response)

    library_notes = parser_book_notes(url, params['id'])
    file_save_name = f'{library_notes["book"]}.{type_file}'
    file_save_path = os.path.join(dir_name, file_save_name)

    with open(file_save_path, 'wb+') as file:
        file.write(response.content)

    return [file_save_path, library_notes]


def parser_book_notes(url: str, book_id: int = None) -> dict:
    book_page_url = urljoin(url, f'b{book_id}')
    response = requests.get(book_page_url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    content = soup.find(id='content')
    title_tag = content.find('h1')
    title_text = title_tag.text.split('::')
    book_image_tag = content.find(class_='bookimage').find('img')

    author = title_text[1].strip()
    book_name = title_text[0].strip()
    book_image_src = urljoin(url, book_image_tag['src'])

    book_notes = {
        'author': author,
        'book': sanitize_filename(book_name),
        'image': book_image_src
    }

    return book_notes
