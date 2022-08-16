import os.path
from pathlib import Path
from urllib.parse import urljoin,  unquote, urlsplit
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    http_code = {200: 'OK'}

    if response.status_code not in http_code:
        raise requests.HTTPError(response.url, response)


def download_txt_file(dir_name: str, url: str, params: dict = None) -> dict:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    type_file = 'txt'
    download_url = urljoin(url, type_file + '.php')

    response = requests.get(download_url, params=params, allow_redirects=False)
    response.raise_for_status()

    check_for_redirect(response)

    library_notes = parser_book_notes(url, params['id'])
    file_save_name = f'{library_notes["book"]}.{type_file}'
    library_notes['book_path'] = os.path.join(dir_name, file_save_name)

    with open(library_notes['book_path'], 'wb+') as file:
        file.write(response.content)

    return library_notes


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
        'book': sanitize_filename(f'{book_id}. {book_name}'),
        'image_url': book_image_src
    }

    return book_notes


def download_img(dir_name: str, url: str):
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    img_name = get_img_full_name(url)

    response = requests.get(url)
    response.raise_for_status()

    file_save_path = os.path.join(dir_name, img_name)

    with open(file_save_path, 'wb') as file:
        file.write(response.content)

    return file_save_path


def get_img_full_name(url: str) -> str:
    img_url = urlsplit(url).path
    unquote_img_url = unquote(img_url)
    img_file = os.path.split(unquote_img_url)[-1]
    img_full_name = "".join(os.path.splitext(img_file))

    return img_full_name