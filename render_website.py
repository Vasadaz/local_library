import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def reload_template():
    with open('library_books.json', 'r', encoding="utf8") as file:
        books = json.load(file)

    books_rows = list(chunked(books.values(), 2))
    template = env.get_template('template.html')
    rendered_page = template.render(books_rows=books_rows)

    with open('index.html', 'w', encoding="utf8") as file:
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
