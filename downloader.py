import os.path
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    http_codes = {200: 'OK'}

    if response.status_code not in http_codes:
        raise requests.HTTPError(response.url, response)


def download_txt(url: str, dir_name: str, book_name: str) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)

    file_type = 'txt'
    book_full_name = '.'.join([book_name, file_type])
    book_save_path = os.path.join(dir_name, book_full_name)

    with open(book_save_path, 'wb+') as file:
        file.write(response.content)

    return book_save_path


def parse_book_page(url: str, book_id: int = None) -> dict:
    book_page_url = urljoin(url, f'b{book_id}/')
    book_download_txt_url = urljoin(url, f'txt.php?id={book_id}')

    response = requests.get(book_page_url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find(id='content')
    title_tag = content.find('h1')
    title_text = title_tag.text.split('::')
    cover_tag = content.find(class_='bookimage').find('img')
    comment_tags = content.find_all('span', class_='black')
    genre_tags = content.find('span', class_='d_book').find_all('a')

    author = title_text[1].strip()
    book_name = title_text[0].strip()
    cover_url = urljoin(url, cover_tag['src'])
    comments = [comment.text for comment in comment_tags]
    genres = [genre.text for genre in genre_tags]

    page_resources = {
        'author': author,
        'book': sanitize_filename(f'{book_id}. {book_name}'),
        'genres': genres,
        'comments': comments,
        'cover_url': cover_url,
        'page_url': book_page_url,
        'txt_url': book_download_txt_url,
    }

    return page_resources


def download_img(url: str, dir_name: str) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    img_name = get_img_full_name(url)

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)

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
