import json

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def reload_template():
    with open('library_books.json', 'r', encoding="utf8") as file:
        books = json.load(file)

    pages_dir_name = 'pages'
    Path(pages_dir_name).mkdir(parents=True, exist_ok=True)

    books_pages = list(chunked(books.values(), 10))

    for page_num, page_books in enumerate(books_pages, 1):
        books_rows = list(chunked(page_books, 2))
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_rows=books_rows,
            page_last_num=len(books_pages),
            page_num=page_num,
        )

        with open(f'{pages_dir_name}/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    reload_template()
    server = Server()
    server.watch('library_books.json', reload_template)
    server.serve(root='.')
