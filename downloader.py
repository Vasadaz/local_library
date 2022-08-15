import urllib.parse
from pathlib import Path

import requests

from bs4 import BeautifulSoup


def check_for_redirect(response):
    http_code = {200: 'OK'}

    if response.status_code not in http_code:
        raise requests.HTTPError(response.url, response)


def download_file(dir_name: str, file_url: str, params: dict = None) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    response = requests.get(file_url, params=params, allow_redirects=False)
    response.raise_for_status()

    check_for_redirect(response)

    file_name = get_file_full_name(response.url)
    file_save_path = f'{dir_name}/{file_name}'

    with open(file_save_path, 'wb+') as file:
        file.write(response.content)

    return file_save_path


def get_file_full_name(url: str) -> str:
    url_blocks = urllib.parse.urlsplit(url)
    file_type = url_blocks.path[1:4]
    file_name = url_blocks.query[3:]
    full_file_name = f'{file_name}.{file_type}'

    return full_file_name


def parser_book_notes(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    content = soup.find(id='content')
    title_tag = content.find('h1')
    title_text = title_tag.text.split('::')
    book_image_tag = content.find(class_='bookimage').find('img')

    author = title_text[1].strip()
    book_name = title_text[0].strip()
    book_image_src = book_image_tag['src']

    book_notes = {
        'author': author,
        'book': book_name,
        'image': book_image_src
    }

    return book_notes
