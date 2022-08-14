import urllib.parse
from pathlib import Path

import requests


def download_file(file_url: str, dir_name: str):
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    file_name = get_file_full_name(file_url)

    response = requests.get(file_url)
    response.raise_for_status()

    file_save_path = f'{dir_name}/{file_name}'

    with open(file_save_path, 'wb') as file:
        file.write(response.content)

    return file_save_path


def get_file_full_name(url: str) -> str:
    url_blocks = urllib.parse.urlsplit(url)
    file_type = url_blocks.path[1:4]
    file_name = url_blocks.query[4:]
    full_file_name = f'{file_name}.{file_type}'

    return full_file_name
