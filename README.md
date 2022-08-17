# Создание локальная библиотека

Проект local_library позволяет скачивает книги по их id из онлайн-библиотеки [tululu](https://tululu.org). 

### Как работает

Скрипт `main.py` является главным. Ему передаются два аргумента `-s / --start_id` и `-e / --end_id` 
с указанием целых чисел, которые обозначает границы диапазона загружаемых книг.
По-умолчанию `START_ID=1` , `END_ID=10`. При успешной загрузке книги в терминале 
будет выведена подробный информация о книги, иначе будет сообщено о невозможности загрузит книга.
Книги сохраняются в директорию `./books` , а обложки к ним в `./covers`. 

#### Аргументы:
```
-h, --help            
 Вывод информации о скрипте
 
-s START_ID, --start_id START_ID
 Начало диапазона id, по-умолчанию 1
 
-e END_ID, --end_id END_ID
 Конец диапазона id, по-умолчанию 10
 ```

#### Пример запуска скрипта `main.py`:
```shell
python main.py -s 6 -e 7
```

#### Пример ответа скрипта `main.py`:
```
Book №6:
author - Зимен Сержио
book - 6. Бархатная революция в рекламе
genres - ['Деловая литература']
comments - ['Очень познавательная книга.', ... , 'Все вокруг да около! Ни слова о сути!']
cover_url - https://tululu.org/shots/6.jpg
page_url - https://tululu.org/b6/
txt_url - https://tululu.org/txt.php?id=6
book_path - books/6. Бархатная революция в рекламе.txt
cover_path - covers/6.jpg

Book №7 Not Found https://tululu.org/txt.php?id=7
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