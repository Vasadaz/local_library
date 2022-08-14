import urllib.parse
from pathlib import Path

import requests


def check_for_redirect(response):
    http_code = {200: 'OK'}

    if response.status_code not in http_code:
        raise requests.HTTPError(response.url, response)


def download_file(dir_name: str, file_url: str, params: dict = None) -> str:
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    response = requests.get(file_url, params=params)
    response.raise_for_status()

    file_name = get_file_full_name(response.url)
    file_save_path = f'{dir_name}/{file_name}'

    try:
        with open(file_save_path, 'wb+') as file:
            file.write(response.content)
    except PermissionError:  # Если такой книги нет
        return (f'Book {params["id"]} Not Found')

    return file_save_path


def get_file_full_name(url: str) -> str:
    url_blocks = urllib.parse.urlsplit(url)
    file_type = url_blocks.path[1:4]
    file_name = url_blocks.query[3:]
    full_file_name = f'{file_name}.{file_type}'

    return full_file_name
