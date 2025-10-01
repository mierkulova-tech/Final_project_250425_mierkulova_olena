"""
                    Модуль для красивого форматирования: вывода результатов поиска
                            жанров, популярных и последних поисковых запросов.
"""

from typing import List, Dict
from datetime import datetime


class ResultFormatter:
    """Класс для форматирования и отображения результатов поиска фильмов и статистики."""
    @staticmethod
    def print_movies(movies: List[Dict]) -> None:
        """
        Вывод списка фильмов с основными данными.
        :param movies: Список словарей с информацией о фильмах
        """
        if not movies:
            print(" Фильмы не найдены")
            return

        for i, movie in enumerate(movies, 1):
            title = f"{i}. {movie['title']} ({movie.get('release_year', 'Н/Д')})"
            rating = movie.get('rating', 'Н/Д')
            length = movie.get('length', 'Н/Д')
            description = movie.get('description', 'Описание отсутствует')

            print(f"{title}")
            print(f"   Рейтинг: {rating} | Длительность: {length} мин")
            print(f"   {description}")
            print("*" * 50)

    @staticmethod
    def print_movies_with_genre(movies: List[Dict]) -> None:
        """
        Вывод списка фильмов с указанием жанра.
        :param movies: Список словарей с информацией о фильмах
        """
        if not movies:
            print("Фильмы не найдены")
            return

        for i, movie in enumerate(movies, 1):
            title = f"{i}. {movie['title']} ({movie.get('release_year', 'Н/Д')})"
            genre = movie.get('genre', 'Н/Д')
            rating = movie.get('rating', 'Н/Д')
            length = movie.get('length', 'Н/Д')
            description = movie.get('description', 'Описание отсутствует')

            print(f"{title}")
            print(f"   Жанр: {genre} | Рейтинг: {rating} | Длительность: {length} мин")
            print(f"   {description}")
            print("*" * 50)

    @staticmethod
    def print_genres(genres: List[Dict]) -> None:
        """Вывод списка жанров в одну колонку с нумерацией."""
        if not genres:
            print("Жанры не найдены")
            return

        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre.get('name', 'Н/Д')}")
        print()

    @staticmethod
    def print_popular_searches(searches: List[Dict]) -> None:
        if not searches:
            print("Данных о популярных запросах пока нет\n")
            return

        print("\n\nТОП ПОПУЛЯРНЫХ ЗАПРОСОВ")
        print("*" * 30)

        for i, search in enumerate(searches, 1):
            search_text = search['search_text']
            count = search['count']
            total_results = search.get('total_results', 0)

            print(f"{i}.'{search_text}'")
            print(f"Поисков: {count} |  Результатов: {total_results}")

            # Показываем дату последнего поиска, если есть
            if 'last_search' in search and search['last_search']:
                last_date = search['last_search']
                if isinstance(last_date, datetime):
                    formatted_date = last_date.strftime("%d.%m.%Y %H:%M")
                    print(f"Последний поиск: {formatted_date}")

            if i < len(searches):
                print("-" * 30)

        print("*" * 30)
        print()  # дополнительный пустой ряд

    @staticmethod
    def print_recent_searches(searches: List[Dict]) -> None:
        if not searches:
            print("Данных о последних запросах пока нет\n")
            return

        print("\n\nПОСЛЕДНИЕ ЗАПРОСЫ")
        print("*" * 30)

        for i, search in enumerate(searches, 1):
            search_text = search['search_text']
            results_count = search.get('results_count', 0)
            timestamp = search.get('timestamp')


            print(f"{i}.'{search_text}'")
            print(f"  Результатов: {results_count}")

            # Показываем время поиска
            if timestamp and isinstance(timestamp, datetime):
                formatted_time = timestamp.strftime("%d.%m.%Y %H:%M:%S")
                print(f"   Время поиска: {formatted_time}")

            if i < len(searches):
                print("-" * 30)

        print("*" * 30)
        print()  # дополнительный пустой ряд
