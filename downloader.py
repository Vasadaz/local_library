import os.path
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError(response.url, response)


def download_txt(url: str, dir_name: str, book_name: str, params: dict = None) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    file_type = 'txt'
    book_full_name = '.'.join([book_name, file_type])
    book_save_path = os.path.join(dir_name, book_full_name)

    with open(book_save_path, 'wb+') as file:
        file.write(response.content)

    return book_save_path


def parse_library_notes(response, book_id: int = None) -> dict:
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find(id='content')
    title_tag = content.find('h1')
    title_texts = title_tag.text.split('::')
    cover_tag = content.find(class_='bookimage').find('img')
    comment_tags = content.find_all('span', class_='black')
    genre_tags = content.find('span', class_='d_book').find_all('a')

    book_name, author = title_texts
    cover_url = cover_tag['src']
    comments = [comment.text for comment in comment_tags]
    genres = [genre.text for genre in genre_tags]

    page_resources = {
        'author': author.strip(),
        'book': sanitize_filename(f'{book_id}. {book_name.strip()}'),
        'genres': genres,
        'comments': comments,
        'cover_url': cover_url,
    }

    return page_resources


def download_img(url: str, dir_name: str) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    img_name = get_img_full_name(url)

    response = requests.get(url)
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
