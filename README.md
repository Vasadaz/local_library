# Создание локальная библиотека

Проект local_library позволяет скачивать книги по их id или по категориям 
из онлайн-библиотеки [tululu.org](https://tululu.org). 

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

# Ответ скрипта:
Parsed 25 books on page 1
Parsed 25 books on page 2

Book №46173 Not Found https://tululu.org/b46173
...
Book №46220 Not Found https://tululu.org/b46220

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