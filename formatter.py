"""
Модуль для красивого форматирования вывода результатов поиска
"""

from typing import List, Dict


class ResultFormatter:
    def print_movies(self, movies: List[Dict]) -> None:
        if not movies:
            print(" Фильмы не найдены")
            return

        for i, movie in enumerate(movies, 1):
            title = f"{i}. {movie['title']} ({movie.get('release_year')})"
            rating = movie.get('rating')
            length = movie.get('length')
            description = movie.get('description', 'Описание отсутствует')
            if len(description) > 100:
                description = description[:100] + "..."

            print("=" * 50)
            print(f" {title}")
            print(f" Рейтинг: {rating} | Длительность: {length} мин")
            print(f" Описание: {description}")
            print()

    def print_movies_with_genre(self, movies: List[Dict]) -> None:
        if not movies:
            print(" Фильмы не найдены")
            return

        for i, movie in enumerate(movies, 1):
            title = f"{i}. {movie.get('title')} ({movie.get('release_year')})"
            genre = movie.get('genre')
            rating = movie.get('rating')
            length = movie.get('length')
            description = movie.get('description', 'Описание отсутствует')
            if len(description) > 100:
                description = description[:100] + "..."

            print("=" * 50)
            print(f" {title}")
            print(f" Жанр: {genre} | Рейтинг: {rating} | Длительность: {length} мин")
            print(f" Описание: {description}")
            print()

    def print_genres(self, genres: List[Dict]) -> None:
        if not genres:
            print("Жанры не найдены")
            return
        for genre in genres:
            print(genre.get('name'))

    def print_popular_searches(self, searches: List[Dict]) -> None:
        print(" ТОП ПОПУЛЯРНЫХ ЗАПРОСОВ")
        print("=" * 50)
        for idx, search in enumerate(searches, 1):
            search_text = search['search_text']
            search_type = search['search_type']
            count = search['count']
            total_results = search['total_results']
            last_search = search['last_search']

            print(f"{idx}. '{search_text}' "
                  f"(тип: {search_type}, "
                  f"раз: {count}, "
                  f"результатов: {total_results}, "
                  f"последний поиск: {last_search})")
