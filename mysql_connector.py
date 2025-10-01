
"""
                Модуль для работы с базой данных фильмов Sakila
"""

import pymysql
from typing import List, Dict, Optional


class MovieDatabase:
    """
    Класс для работы с базой данных фильмов Sakila.
    Умеет подключаться, выполнять запросы и предоставлять данные о фильмах.
    """

    def __init__(self):
        """
        Инициализация объекта и автоматическое подключение к базе данных.
        """
        self.connection = None
        self.connect()

    def connect(self):
        """
        Подключается к базе данных MySQL с использованием PyMySQL.
        """
        self.connection = pymysql.connect(
            host='ich-db.edu.itcareerhub.de',
            user='ich1',
            password='password',
            database='sakila',
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Выполняет SQL-запрос и возвращает все результаты.

        Args:
            query (str): SQL-запрос с параметрами.
            params (tuple, optional): параметры для запроса.

        Returns:
            List[Dict]: список словарей с результатами запроса.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def search_by_keyword(self, keyword: str, offset: int = 0, limit: int = 10) -> List[Dict]:
        """
        Поиск фильмов по ключевому слову в названии и описании.

        Args:
            keyword (str): слово для поиска.
            offset (int): смещение для пагинации.
            limit (int): максимальное количество фильмов.

        Returns:
            List[Dict]: список найденных фильмов.
        """
        query = """
        SELECT 
            f.film_id,
            f.title,
            f.release_year,
            f.description,
            f.rating,
            f.length
        FROM film f
        WHERE 
            f.title LIKE %s 
            OR f.description LIKE %s
        ORDER BY f.title
        LIMIT %s OFFSET %s
        """

        search_pattern = f"%{keyword}%"
        params = (search_pattern, search_pattern, limit, offset)

        return self.execute_query(query, params)

    def search_by_genre_and_year(self, genre: str, year_from: int,
                                 year_to: int, offset: int = 0, limit: int = 10) -> List[Dict]:
        """
        Поиск фильмов по жанру и диапазону годов выпуска.

        Args:
            genre (str): жанр фильмов.
            year_from (int): год начала диапазона.
            year_to (int): год конца диапазона.
            offset (int): смещение для пагинации.
            limit (int): максимальное количество фильмов.

        Returns:
            List[Dict]: список найденных фильмов.
        """
        query = """
        SELECT 
            f.film_id,
            f.title,
            f.release_year,
            f.description,
            f.rating,
            f.length,
            c.name as genre
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE 
            c.name = %s 
            AND f.release_year BETWEEN %s AND %s
        ORDER BY f.release_year DESC, f.title
        LIMIT %s OFFSET %s
        """

        params = (genre, year_from, year_to, limit, offset)
        return self.execute_query(query, params)

    def get_all_genres(self) -> List[Dict]:
        """
        Получить список всех жанров из базы данных.

        Returns:
            List[Dict]: список жанров с id и названием.
        """
        query = """
        SELECT 
            category_id,
            name
        FROM category
        ORDER BY name
        """

        return self.execute_query(query)

    def get_year_range(self) -> Dict[str, int]:
        """
        Получить минимальный и максимальный год выпуска фильмов.

        Returns:
            Dict[str, int]: словарь с ключами 'min' и 'max' для годов.
        """
        query = """
        SELECT 
            MIN(release_year) as min_year,
            MAX(release_year) as max_year
        FROM film
        """

        result = self.execute_query(query)
        if result:
            return {
                'min': result[0]['min_year'],
                'max': result[0]['max_year']
            }
        return {'min': 2006, 'max': 2006}

    def get_movie_details(self, film_id: int) -> Optional[Dict]:
        """
        Получить подробную информацию по фильму по его ID.

        Args:
            film_id (int): уникальный идентификатор фильма.

        Returns:
            Optional[Dict]: словарь с деталями фильма или None.
        """
        query = """
        SELECT 
            f.*,
            GROUP_CONCAT(c.name) as genres,
            COUNT(fa.actor_id) as actor_count
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        WHERE f.film_id = %s
        GROUP BY f.film_id
        """

        result = self.execute_query(query, (film_id,))
        return result[0] if result else None


    def close(self):
        """
        Закрыть соединение с базой данных.
        """
        if self.connection:
            self.connection.close()
