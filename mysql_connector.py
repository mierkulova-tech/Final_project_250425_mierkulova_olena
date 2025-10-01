
"""
                Модуль для работы с базой данных фильмов Sakila
"""
import os
import pymysql
from pymysql import MySQLError
from typing import List, Dict


class MovieDatabase:
    """Класс для работы с базой данных фильмов Sakila."""
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Подключение к базе данных MySQL."""
        try:
            self.connection = pymysql.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE'),
                charset='utf8mb4',
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception:
            raise  # Ошибки печатает MovieSearchApp

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Выполняет SQL-запрос к базе данных и возвращает список словарей.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except MySQLError as e:
            print(f"Ошибка выполнения запроса: {e}")
            raise

    def search_by_keyword(self, keyword: str, offset: int = 0, limit: int = 10) -> List[Dict]:
        """Поиск фильмов по ключевому слову с пагинацией."""
        query = """
        SELECT film_id, title, release_year, description, rating, length
        FROM film
        WHERE title LIKE %s OR description LIKE %s
        ORDER BY title
        LIMIT %s OFFSET %s
        """
        pattern = f"%{keyword}%"
        return self.execute_query(query, (pattern, pattern, limit, offset))

    def search_by_genre_and_year(self, genre: str, year_from: int,
                                 year_to: int, offset: int = 0, limit: int = 10) -> List[Dict]:
        """Поиск фильмов по жанру и диапазону лет с пагинацией."""
        query = """
                SELECT f.film_id, f.title, f.release_year, f.description, f.rating, f.length, c.name as genre
                FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                JOIN category c ON fc.category_id = c.category_id
                WHERE c.name = %s AND f.release_year BETWEEN %s AND %s
                ORDER BY f.release_year DESC, f.title
                LIMIT %s OFFSET %s
                """
        return self.execute_query(query, (genre, year_from, year_to, limit, offset))

    def get_all_genres(self) -> List[Dict]:
        """Возвращает список всех жанров"""
        query = "SELECT category_id, name FROM category ORDER BY name"
        return self.execute_query(query)

    def get_year_range(self) -> Dict[str, int]:
        """Возвращает минимальный и максимальный год выпуска фильмов"""
        query = "SELECT MIN(release_year) as min_year, MAX(release_year) as max_year FROM film"
        result = self.execute_query(query)
        return {'min': result[0]['min_year'], 'max': result[0]['max_year']}

    def close(self):
        """Закрывает соединение с базой данных"""
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Ошибка закрытия подключения: {e}")