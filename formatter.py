"""
                    Модуль для красивого форматирования вывода результатов поиска
"""

from typing import List, Dict, Any
from datetime import datetime


class ResultFormatter:
    def __init__(self):
        self.width = 80  # Ширина таблиц

    def print_movies(self, movies: List[Dict]) -> None:
        if not movies:
            print(" Фильмы не найдены")
            return

        print("+" + "-" * (self.width - 2) + "+")

        for i, movie in enumerate(movies, 1):
            # Заголовок фильма
            title = f"{i}. {movie['title']} ({movie['release_year'] or 'Н/Д'})"
            rating = movie.get('rating', 'Н/Д')
            length = movie.get('length', 'Н/Д')

            print(f"| {title:<{self.width - 4}} |")

            # Информация о фильме
            info = f"    Рейтинг: {rating} |  Длительность: {length} мин"
            print(f"| {info:<{self.width - 4}} |")

            # Описание (обрезаем если слишком длинное)
            description = movie.get('description', 'Описание отсутствует')
            if len(description) > self.width - 8:
                description = description[:self.width - 11] + "..."

            desc_line = f"    {description}"
            print(f"| {desc_line:<{self.width - 4}} |")

            # Разделитель между фильмами
            if i < len(movies):
                print("|" + "-" * (self.width - 2) + "|")

        print("+" + "-" * (self.width - 2) + "+")

    def print_movies_with_genre(self, movies: List[Dict]) -> None:
        if not movies:
            print("Фильмы не найдены")
            return

        print("+" + "-" * (self.width - 2) + "+")

        for i, movie in enumerate(movies, 1):
            # Заголовок фильма
            title = f"{i}. {movie['title']} ({movie['release_year'] or 'Н/Д'})"
            print(f"| {title:<{self.width - 4}} |")

            # Информация о фильме с жанром
            rating = movie.get('rating', 'Н/Д')
            length = movie.get('length', 'Н/Д')
            genre = movie.get('genre', 'Н/Д')

            info = f"    {genre} |  {rating} |  {length} мин"
            print(f"| {info:<{self.width - 4}} |")

            # Описание
            description = movie.get('description', 'Описание отсутствует')
            if len(description) > self.width - 8:
                description = description[:self.width - 11] + "..."

            desc_line = f"    {description}"
            print(f"| {desc_line:<{self.width - 4}} |")

            # Разделитель между фильмами
            if i < len(movies):
                print("|" + "-" * (self.width - 2) + "|")

        print("+" + "-" * (self.width - 2) + "+")

    def print_genres(self, genres: List[Dict]) -> None:
        if not genres:
            print(" Жанры не найдены")
            return

        # Выводим жанры по 3 в ряд для экономии места
        cols = 3
        for i in range(0, len(genres), cols):
            row_genres = genres[i:i + cols]
            genre_line = ""

            for j, genre in enumerate(row_genres):
                # Вычисляем сквозной номер жанра
                genre_number = i + j + 1
                genre_name = genre['name']

                # Форматируем строку: Номер. Имя_Жанра
                # Используем отступ 30 символов, чтобы поместился номер и название
                genre_entry = f"{genre_number}. {genre_name}"
                genre_line += f" {genre_entry:<30}"

                # Добавляем разделитель, если это не последний элемент в ряду
                if j < len(row_genres) - 1:
                    genre_line += " | "

            print(genre_line)

    def print_popular_searches(self, searches: List[Dict]) -> None:
        if not searches:
            print("Данных о популярных запросах пока нет")
            return

        print(" ТОП ПОПУЛЯРНЫХ ЗАПРОСОВ")
        print("=" * 50)

        for i, search in enumerate(searches, 1):
            search_text = search['search_text']
            count = search['count']
            search_type = search['search_type']
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

        print("=" * 50)

    def print_recent_searches(self, searches: List[Dict]) -> None:
        if not searches:
            print("Данных о последних запросах пока нет")
            return

        print("ПОСЛЕДНИЕ ЗАПРОСЫ")
        print("=" * 50)

        for i, search in enumerate(searches, 1):
            search_text = search['search_text']
            search_type = search['search_type']
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

        print("=" * 50)

    def print_search_stats(self, stats: Dict[str, Any]) -> None:
        print("ОБЩАЯ СТАТИСТИКА")
        print("=" * 40)

        for key, value in stats.items():
            # Красивые названия для ключей
            readable_keys = {
                'total_searches': 'Всего поисков',
                'keyword_searches': 'Поиск по словам',
                'genre_year_searches': 'Поиск по жанрам',
                'empty_searches': 'Пустых результатов'
            }

            readable_key = readable_keys.get(key, key)
            print(f"{readable_key}: {value}")

        print("=" * 40)

    def print_error_message(self, message: str) -> None:
        print("\n" + "X " + "=" * 50 + " X")
        print(f" ОШИБКА: {message}")
        print("X" + "=" * 50 + " 🚨\n")

    def print_success_message(self, message: str) -> None:
        print("\n" + "ok" + "=" * 50 + "ok")
        print(f" {message}")
        print("ok" + "=" * 50 + " ok\n")

    def print_info_message(self, message: str) -> None:
        print(f"\n {message}\n")

    def truncate_text(self, text: str, max_length: int = 50) -> str:
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."


def test_formatter():
    formatter = ResultFormatter()
    print("Тестирование форматтера результатов\n")

    test_movies = [
        {
            'title': 'The Matrix',
            'release_year': 1999,
            'rating': 'R',
            'length': 136,
            'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.'
        },
        {
            'title': 'Avatar',
            'release_year': 2009,
            'rating': 'PG-13',
            'length': 162,
            'description': 'A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.'
        }
    ]

    print("Тест вывода фильмов:")
    formatter.print_movies(test_movies)

    test_genres = [
        {'name': 'Action'}, {'name': 'Comedy'}, {'name': 'Drama'},
        {'name': 'Horror'}, {'name': 'Sci-Fi'}, {'name': 'Romance'}
    ]

    print("\n Тест вывода жанров:")
    formatter.print_genres(test_genres)

    test_popular = [
        {
            'search_text': 'matrix',
            'count': 15,
            'search_type': 'keyword',
            'total_results': 3,
            'last_search': datetime.now()
        },
        {
            'search_text': 'action 2000-2010',
            'count': 8,
            'search_type': 'genre_year',
            'total_results': 25
        }
    ]

    print("\n Тест популярных запросов:")
    formatter.print_popular_searches(test_popular)

    print("\n Тестирование форматтера завершено!")


if __name__ == "__main__":
    test_formatter()