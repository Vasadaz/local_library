import json

from pathlib import Path, PurePosixPath

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

PAGES_DIR_NAME = 'pages'


def convert_txt_to_html(txt_path: str) -> PurePosixPath:
    global PAGES_DIR_NAME
    txt_path = Path(txt_path)

    html_book_path = PurePosixPath(PAGES_DIR_NAME) / 'html_books' / (txt_path.stem + '.html')

    Path(html_book_path.parents[0]).mkdir(parents=True, exist_ok=True)

    template = env.get_template('book.html')
    rendered_page = template.render(
        book=txt_path.read_text(encoding='utf8'),
        title=txt_path.stem
    )

    with open(f'{html_book_path}', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    return html_book_path.relative_to(PAGES_DIR_NAME)


def reload_template():
    global PAGES_DIR_NAME

    with open('library_books.json', 'r', encoding='utf8') as file:
        books = json.load(file)

    bookshelf_number = 10
    books_on_bookshelf_number = 2
    Path(PAGES_DIR_NAME).mkdir(parents=True, exist_ok=True)

    books_pages = list(chunked(books.values(), bookshelf_number))

    for page_num, page_books in enumerate(books_pages, 1):
        books_rows = list(chunked(page_books, books_on_bookshelf_number))
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_rows=books_rows,
            page_last_num=len(books_pages),
            page_num=page_num,
        )

        with open(f'{PAGES_DIR_NAME}/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    env.filters['convert'] = convert_txt_to_html

    reload_template()
    server = Server()
    server.watch('library_books.json', reload_template)
    server.serve(root='.')
