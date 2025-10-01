### 🎬 Movie Search App - MierX-

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Logs-green?logo=mongodb&logoColor=white)
![Status](https://img.shields.io/badge/Project-Final_Project_250425_ptm-success)

---

## 📌 Что делает приложение

- 🔍 **Поиск по ключевому слову** — находит фильмы по названию или описанию  
- 🎭 **Поиск по жанру и годам** — фильтрует фильмы по жанру и диапазону лет  
- 📊 **Статистика запросов** — показывает популярные и последние поиски  
- 🗄 **Логирование** — сохраняет все запросы в MongoDB для анализа  

---

## ⚙️ Технологии

- **Python 3.8+**
- **MySQL** (база данных Sakila с фильмами)
- **MongoDB** (для хранения логов поиска)
- **pymysql** (подключение к MySQL)
- **pymongo** (подключение к MongoDB)

---

## 🖥 Системные требования

- Python 3.8 или выше  
- MySQL Server с базой данных **Sakila**  
- MongoDB Server  

### 📦 Установка Python-пакетов

```bash
pip install pymysql pymongo python-dotenv

---

## 🔒 Настройка подключений

Все учетные данные хранятся в файле **.env** в корневой папке проекта.  

### Создание `.env`

```env
# ------------------------------------
# --- MySQL/Sakila Настройки ---
# ------------------------------------
MYSQL_HOST=ich-db.edu.itcareerhub.de
MYSQL_USER=ich1
MYSQL_PASSWORD=ВАШ_ПАРОЛЬ_MYSQL
MYSQL_DATABASE=sakila

# ------------------------------------
# --- MongoDB Настройки ---
# ------------------------------------
MONGO_URI="mongodb://ich_editor:ВАШ_ПАРОЛЬ_MONGO@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"

MONGO_DATABASE=ich_edit
MONGO_COLLECTION=Final_project_250425_mierkulova_olena
```

> ⚠️ Замените `ВАШ_ПАРОЛЬ_MYSQL` и `ВАШ_ПАРОЛЬ_MONGO` на актуальные данные.  

---

## 🚀 Как пользоваться

### Главное меню

```
MOVIE SEARCH APP - MierX-
==================================================
1. Поиск по ключевому слову
2. Поиск по жанру и годам  
3. Популярные запросы
4. Последние запросы
5. Выйти
==================================================
```

#### 🔍 Поиск по ключевому слову  
- Введите слово (например: `matrix`, `love`, `war`)  
- Найдет фильмы по названию и описанию  
- Показ по 10 результатов с возможностью пролистывания  

#### 🎭 Поиск по жанру и годам  
- Список доступных жанров  
- Диапазон лет из базы  
- Введите жанр и диапазон лет (например: `Action`, 2000–2010)  

#### 📊 Статистика  
- ⭐ **Популярные запросы** — самые частые  
- 🕒 **Последние запросы** — свежие уникальные  

---

## 📂 Структура проекта

```
movie_search_project/
├── main.py              # Главный файл приложения
├── mysql_connector.py   # Работа с MySQL (поиск фильмов)
├── log_writer.py        # Запись логов в MongoDB
├── log_stats.py         # Статистика логов из MongoDB  
├── formatter.py         # Красивый вывод результатов
├── README.md            # Эта инструкция
├── .env                 # Конфигурация
└── .gitignore           # Игнорируемые файлы
```

---

## 🔑 Основные функции

### MovieDatabase (mysql_connector.py)
- `search_by_keyword()` — поиск по ключевому слову  
- `search_by_genre_and_year()` — поиск по жанру и годам  
- `get_all_genres()` — все жанры  
- `get_year_range()` — диапазон лет  

### LogWriter (log_writer.py) 
- `log_search()` — записать запрос  
- `get_logs_count()` — количество логов  
- `clear_logs()` — очистить логи  

### LogStats (log_stats.py)
- `get_popular_searches()` — популярные запросы  
- `get_recent_searches()` — последние запросы  
- `get_search_stats_by_type()` — статистика по типам  

### ResultFormatter (formatter.py)
- `print_movies()` — красивый вывод фильмов  
- `print_popular_searches()` — популярные запросы  
- `print_recent_searches()` — последние запросы  

---

## 🌟 Дополнительные возможности

- 📑 **Пагинация** — просмотр результатов по 10  
- 🛡 **Обработка ошибок** — приложение не падает  
- 🗄 **Логирование** — сохранение всех запросов  
- 📊 **Статистика** — анализ поисковой активности  

---

## 👩‍💻 Автор

- **Студентка**: Mierkulova Olena  
- **Группа**: 250425 ptm  
- **Проект**: Final Project — *Movie Search App - MierX-*  
