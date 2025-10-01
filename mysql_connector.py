
"""
                Модуль для работы с базой данных фильмов Sakila
"""

import pymysql
from typing import List, Dict, Optional, Any
import os

class MovieDatabase:

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
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
            #print(" Подключение к MySQL успешно!")

        except Exception as e:
            print(f" Ошибка подключения к Базе Фильмов: {e}") # Оставляем для отладки
            raise

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

        except Exception as e:
            print(f" Ошибка выполнения запроса: {e}")
            raise

    def search_by_keyword(self, keyword: str, offset: int = 0, limit: int = 10) -> List[Dict]:
        """
            Ищет фильмы по ключевому слову в названии или описании.
            Использует LIKE %s для гибкого поиска.
            LIMIT и OFFSET нужны для пагинации (показа результатов по 10 штук).
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
            Получает минимальный и максимальный год выпуска фильмов в базе данных
            для ограничения поиска по годам.
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

        query = """
        SELECT 
            category_id,
            name
        FROM category
        ORDER BY name
        """

        return self.execute_query(query)

    def get_year_range(self) -> Dict[str, int]:

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

    def test_connection(self) -> bool:

        try:
            result = self.execute_query("SELECT 1 as test")
            return len(result) > 0

        except Exception:
            return False

    def get_database_stats(self) -> Dict[str, Any]:

        stats = {}

        try:
            # Количество фильмов
            result = self.execute_query("SELECT COUNT(*) as count FROM film")
            stats['total_films'] = result[0]['count']

            # Количество жанров
            result = self.execute_query("SELECT COUNT(*) as count FROM category")
            stats['total_genres'] = result[0]['count']

            # Количество актеров
            result = self.execute_query("SELECT COUNT(*) as count FROM actor")
            stats['total_actors'] = result[0]['count']

        except Exception as e:
            print(f" Ошибка получения статистики: {e}")

        return stats

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                print(" Подключение к MySQL закрыто")
        except Exception as e:
            print(f" Ошибка закрытия подключения к MySQL: {e}")



def test_mysql_connection():
    try:
        db = MovieDatabase()

        print(" Тестирование подключения...")
        if db.test_connection():
            print(" Подключение работает!")
        else:
            print(" Проблемы с подключением!")
            return

        print("\n Статистика базы данных:")
        stats = db.get_database_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print("\n Тестирование поиска по ключевому слову:")
        movies = db.search_by_keyword("Matrix", 0, 3)
        for movie in movies:
            print(f"  - {movie['title']} ({movie['release_year']})")

        print("\n Диапазон лет:")
        year_range = db.get_year_range()
        print(f"  {year_range['min']} - {year_range['max']}")

        print("\n Жанры (первые 5):")
        genres = db.get_all_genres()[:5]
        for genre in genres:
            print(f"  - {genre['name']}")

        db.close()
        print("\n Тест завершен успешно!")

    except Exception as e:
        print(f" Ошибка тестирования: {e}")


if __name__ == "__main__":
    test_mysql_connection()