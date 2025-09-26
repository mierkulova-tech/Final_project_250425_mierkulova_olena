                        Movie Search App -MierX-
                    интерактивное консольное приложение

Что делает приложение

Искать фильмы:
Поиск по ключевому слову: Находит фильмы по названию или описанию
Поиск по жанру и годам: Фильтрует фильмы по жанру и диапазону лет
Статистика запросов: Показывает популярные и последние поиски
Логирование Сохраняет все запросы в MongoDB для анализа

Технологии

Технологии
● Python
● MySQL (данные о фильмах)
● MongoDB (логирование запросов)
● pymysql, pymongo, другие модули (например для вывода в консоль)

 Системные требования
- Python 3.8 или выше
- MySQL Server с базой данных Sakila
- MongoDB Server

Python пакеты
```
pip install pymysql pymongo
```


Настройка подключений

В файле `mysql_connector.py`:
```
self.connection = pymysql.connect(
    host='ich-db.edu.itcareerhub.de',
    user='ich1',
    password='password',
    database='sakila',
)
```
В файлах `log_writer.py` и `log_stats.py`:
```
mongodb_uri = "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit" 
collection_name = "Final_project_250405_mierkulova_olena"
```

Как пользоваться

Главное меню
```
MOVIE SEARCH APP -MierX-
==================================================
1. Поиск по ключевому слову
2. Поиск по жанру и годам  
3. Популярные запросы
4. Выйти
==================================================
```

1. Поиск по ключевому слову
- Введите любое слово (например: "matrix", "love", "war")
- Приложение найдет фильмы по названию и описанию
- Результаты показываются по 10 штук
- Можно просматривать следующие 10 результатов

2. Поиск по жанру и годам
- Сначала увидите все доступные жанры
- Увидите диапазон лет в базе данных
- Введите жанр (например: "Action", "Comedy")
- Введите диапазон лет (например: с 2000 до 2010)

3. Статистика
- **Популярные запросы**: Самые часто искомые слова/фразы

Структура проекта

```
movie_search_project/
├── movie_search_main.py   # Главный файл приложения
├── mysql_connector.py     # Работа с MySQL (поиск фильмов)
├── log_writer.py          # Запись логов в MongoDB
├── log_stats.py           # Статистика логов из MongoDB  
├── formatter.py           # Красивый вывод результатов
└── README.md              # Эта инструкция
```

Основные функции

MovieDatabase (mysql_connector.py)
- `search_by_keyword()` - поиск по ключевому слову
- `search_by_genre_and_year()` - поиск по жанру и годам
- `get_all_genres()` - получить все жанры
- `get_year_range()` - диапазон лет в базе

LogWriter (log_writer.py) 
- `log_search()` - записать поисковый запрос
- `get_logs_count()` - количество логов


LogStats (log_stats.py)
- `get_popular_searches()` - популярные запросы
- `get_search_stats_by_type()` - статистика по типам

ResultFormatter (formatter.py)
- `print_movies()` - красивый вывод фильмов
- `print_popular_searches()` - вывод популярных запросов


Дополнительные возможности

- **Пагинация**: Просмотр результатов по 10 штук
- **Обработка ошибок**: Программа не падает при проблемах
- **Логирование**: Все поиски сохраняются для анализа
- **Статистика**: Анализ популярности запросов

Автор

**Студентка**: Mierkulova Olena
**Группа**: 250425
**Проект**: Final Project - Movie Search App -MierX-

---
