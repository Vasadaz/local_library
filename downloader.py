from pathlib import Path, PurePosixPath
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_img(url: str, dir_name: str) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    img_name = PurePosixPath(url).name

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    file_save_path = PurePosixPath(dir_name) / img_name

    with open(file_save_path, 'wb') as file:
        file.write(response.content)

    return file_save_path.as_posix()


def download_txt(url: str, dir_name: str, book_name: str, params: dict = None) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    file_type = 'txt'
    book_full_name = '.'.join([book_name, file_type])
    book_save_path = PurePosixPath(dir_name) / book_full_name

    with open(book_save_path, 'wb+') as file:
        file.write(response.content)

    return book_save_path.as_posix()


def parse_library_notes(response, book_id: int = None) -> dict:
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.select_one('#content h1')
    title_texts = title_tag.text.split('::')
    cover_tag = soup.select_one('#content .bookimage img')
    comment_tags = soup.select('#content .black')
    genre_tags = soup.select('#content .d_book a[title*="жанр"]')

    book_name, author = title_texts
    cover_url = urljoin(response.url, cover_tag['src'])
    comments = [comment.text for comment in comment_tags]
    genres = [genre.text for genre in genre_tags]

    page_resources = {
        'author': author.strip(),
        'name': sanitize_filename(f'{book_id} {book_name.strip()}'),
        'genres': genres,
        'comments': comments,
        'cover_url': cover_url,
    }

    return page_resources
