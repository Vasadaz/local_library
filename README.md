# Локальная библиотека в браузере

Проект local_library позволяет скачивать книги по их id или по категориям 
из онлайн-библиотеки [tululu.org](https://tululu.org), а также создаёт 
локальный сайт библиотеки - [пример сайта](https://vasadaz.github.io/local_library/).


### Как работает `main.py`

Скрипт скачивает книги по их id из онлайн-библиотеки [tululu.org](https://tululu.org).
При успешной загрузке книги в терминале будет выведена подробная информация, 
иначе будет сообщено о невозможности загрузить файл.
Книги сохраняются в директорию `./books`, а обложки к ним в `./covers`.


###### Аргументы `main.py`:
```
-h, --help            
    Вывод информации о скрипте
 
-s START_ID, --start_id START_ID
    Начало диапазона id, по-умолчанию 1
 
-e END_ID, --end_id END_ID
    Конец диапазона id, по-умолчанию 10
 ```


###### Пример запуска скрипта `main.py`:
```shell
python main.py -s 6 -e 7

# Ответ скрипта:
Book №6:
author - Зимен Сержио
name - 6. Бархатная революция в рекламе
genres - ['Деловая литература']
comments - ['Книга для настоящий рекламщиков!', ... , 'Все вокруг да около! Ни слова о сути!']
book_path - books/6. Бархатная революция в рекламе.txt
cover_path - covers/6.jpg

Book №7 Not Found https://tululu.org/txt.php?id=7

# Результат запуска:
local_library/
├── books/
│   └── 6. Бархатная революция в рекламе.txt
└── covers/
    └── 6.jpg
```


### Как работает `parse_tululu_category.py`

Скрипт для скачивания книг из указанной категории онлайн-библиотеки [tululu.org](https://tululu.org).
Книги сохраняются в директорию `./books`, а обложки к ним в `./covers`. 
Вся информация по книгам сохраняется в JSON файл - `library_books.json`.


###### Аргументы `parse_tululu_category.py`:
```
-h, --help            
    Вывод информации о скрипте
    
-c CATEGORY_URL, --category_url CATEGORY_URL
    Ссылка на категорию, по умолчанию категория "Научная фантастика" https://tululu.org/l55/
 
-s START_PAGE, --start_page START_PAGE
    Начало диапазона страниц, по-умолчанию 1
 
-e END_PAGE, --end_page END_PAGE
    Конец диапазона страниц, по-умолчанию последняя страница
 
--dest_folder DEST_FOLDER
    Указание пути к каталогу с результатами парсинга: картинкам, книгам, JSON.
  
--skip_imgs
    Скрипт не будет скачивать картинки
  
--skip_txt
    Скрипт не будет скачивать книги
  
--json_path JSON_PATH
    Указание пути к JSON файлу с информацией по книгам. Если указан
    --dest_folder, то итоговый путь JSON файла:
    DEST_FOLDER/JSON_PATH/library_books.json
 ```


###### Пример запуска скрипта `parse_tululu_category.py`:

```shell
python parse_tululu_category.py -c https://tululu.org/computer/ -s 1 -e 2 --json_path result --skip_img --dest_folder fantastic

# Ответ от скрипта в случае отсутствия файла txt на tululu.org:
Resource Not Found: function get_book_resources({'book_id': '46173', 'get_cover': False, 'get_txt': True})
...
Resource Not Found: function get_book_resources({'book_id': '46220', 'get_cover': False, 'get_txt': True})

# Результат запуска:
local_library/
└── fantastic/
    ├── books/
    │   ├── 46168. 1.Внутреннее устройство Windows (гл. 1-4).txt
    │   ├── ...
    │   └── 46236. Все под контролем Кто и как следит за тобой.txt
    └── result/
        └── library_books.json
```


### Как работает `render_website.py`

На основании файла `library_books.json` скрипт создаёт локальный сайт библиотеки, 
который доступен в браузере по адресу [127.0.0.1:5500](http://127.0.0.1:5500) -
[пример сайта](https://vasadaz.github.io/local_library/).


###### Пример запуска скрипта `render_website.py`:

```shell
python render_website.py

# Ответ скрипта:
[I 220911 22:11:27 server:335] Serving on http://127.0.0.1:5500
[I 220911 22:11:27 handlers:62] Start watching changes
[I 220911 22:11:27 handlers:64] Start detecting changes
```


### Как установить

Python3 должен быть уже установлен. 

Для установки зависимостей используйте:
```shell
pip install -r requirements.txt
```
Если есть конфликт с Python2 используйте:
```shell
pip3 install -r requirements.txt
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
