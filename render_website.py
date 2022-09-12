import json

from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape, filters
from livereload import Server
from more_itertools import chunked


def reload_template():
    with open('library_books.json', 'r', encoding="utf8") as file:
        books = json.load(file)

    bookshelf_number = 10
    books_on_bookshelf_number = 2
    pages_dir_name = 'pages'
    Path(pages_dir_name).mkdir(parents=True, exist_ok=True)

    books_pages = list(chunked(books.values(), bookshelf_number))

    for page_num, page_books in enumerate(books_pages, 1):
        books_rows = list(chunked(page_books, books_on_bookshelf_number))
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_rows=books_rows,
            page_last_num=len(books_pages),
            page_num=page_num,
        )
        print(quote(books_rows[0][0]['book_path']))

        with open(f'{pages_dir_name}/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    reload_template()
    server = Server()
    server.watch('library_books.json', reload_template)
    server.serve(root='.')
