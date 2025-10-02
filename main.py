"""
                                            "MierX"
                                        Movie Search App
                        Приложение для поиска фильмов с логированием в MongoDB
"""
from pymongo.errors import PyMongoError, ConnectionFailure
from pymysql import MySQLError, OperationalError
from mysql_connector import MovieDatabase
from log_writer import LogWriter
from log_stats import LogStats
from formatter import ResultFormatter
import sys
from dotenv import load_dotenv


class MovieSearchApp:
    def __init__(self):
        load_dotenv()
        print("Запускаем Movie Search App -MierX- ...")

        try:
            self.movie_db = MovieDatabase()
            self.logger = LogWriter()
            self.stats = LogStats()
            self.formatter = ResultFormatter()

        except OperationalError:
            print("Не удалось подключиться к MySQL серверу:")
            print("Проверьте: доступен ли сервер, правильные ли логин/пароль")
            sys.exit(1)

        except MySQLError:
            print("Внутренняя ошибка MySQL. Попробуйте повторить запрос позже.")
            sys.exit(1)

        except ConnectionFailure:
            print("Не удалось подключиться к MongoDB. Проверьте сервер и настройки подключения.")
            sys.exit(1)

    def show_main_menu(self):
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print(" MOVIE SEARCH APP  -MierX- ")
        print("=" * 50)
        print("1.  Поиск по ключевому слову")
        print("2.  Поиск по жанру и годам")
        print("3.  Популярные запросы")
        print("4.  Последние запросы")
        print("5.  Выйти")
        print("=" * 50)

    def search_by_keyword(self):
        keyword = input("Введите ключевое слово: ").strip()
        if not keyword:
            print("Вы ничего не ввели. Пожалуйста, введите слово для поиска.")
            return
        if len(keyword) < 2:
            print("Слишком короткий запрос. Нужно хотя бы 2 символа.")
            return

        keyword = keyword.lower()
        offset = 0

        while True:
            try:
                movies = self.movie_db.search_by_keyword(keyword, offset)
            except (MySQLError, PyMongoError):
                print("При поиске произошла ошибка. Попробуйте позже.")
                return

            if not movies:
                if offset == 0:
                    print(f"По запросу '{keyword}' ничего не найдено")
                    # Логируем даже пустые результаты для статистики (популярные, но неуспешные запросы)
                    # Например, что пользователи ищут и чего не хватает в базе - будет запись в логгах.
                    self.logger.log_keyword_search(keyword, 0)
                else:
                    print("Больше результатов нет")
                break

            # Показываем результаты
            print(f"\n Найдено фильмов (показаны {offset + 1}-{offset + len(movies)}):")
            self.formatter.print_movies(movies)

            # Логируем поиск только при первых результатах
            if offset == 0:
                self.logger.log_keyword_search(keyword, len(movies))

            # Спрашиваем про продолжение, пагинация
            if len(movies) == 10:  # Если получили полную страницу
                choice = input("\n Показать следующие 10? (y/n): ").lower()
                if choice != 'y':
                    break
                offset += 10
            else:
                break

    def search_by_genre_and_year(self):
        # Показываем доступные жанры
        try:
            genres = self.movie_db.get_all_genres()
            year_range = self.movie_db.get_year_range()
        except (MySQLError, PyMongoError):
            print("Не удалось получить данные для поиска. Попробуйте позже.")
            return

        print("Доступные жанры:")
        self.formatter.print_genres(genres)
        print(f"\nДиапазон лет: {year_range['min']} - {year_range['max']}")

        # Запрашиваем жанр
        genre = input("\nВведите жанр: ").strip()
        if not genre:
            print("Жанр не может быть пустым!")
            return
        # Проверяем, существует ли жанр
        if genre not in [g['name'] for g in genres]:
            print(f" Жанр '{genre}' не найден!")
            return

        # Запрашиваем годы
        try:
            year_from = int(input("Год с (например 1990): "))
            year_to = int(input("Год до (например 2025): "))
            if year_from > year_to:
                print("Год 'с' не может быть больше года 'до'!")
                return
        except ValueError:
            print("Годы должны быть числами!")
            return

        # Поиск с пагинацией
        offset = 0
        search_params = {"genre": genre,"year_from": year_from,"year_to": year_to}

        while True:
            try:
                movies = self.movie_db.search_by_genre_and_year(genre, year_from, year_to, offset)
            except (MySQLError, PyMongoError):
                print("При поиске произошла ошибка. Попробуйте позже.")
                return

            if not movies:
                if offset == 0:
                    print("По запросу не найдено фильмов")
                    self.logger.log_genre_year_search(genre, year_from, year_to, 0)
                else:
                    print("Больше результатов нет")
                break

            # Показываем результаты
            print(f"\n Найдено фильмов (показаны {offset + 1}-{offset + len(movies)}):")
            self.formatter.print_movies_with_genre(movies)

            # Логируем только первые результаты
            if offset == 0:
                self.logger.log_genre_year_search(genre, year_from, year_to, len(movies))

            # Проверяем продолжение
            if len(movies) == 10:
                choice = input("\n Показать следующие 10? (y/n): ").lower()
                if choice != 'y':
                    break
                offset += 10
            else:
                break

    def show_popular_searches(self):
        """Показать популярные запросы"""
        try:
            popular = self.stats.get_popular_searches(5)
        except (MySQLError, PyMongoError):
            print("Не удалось получить статистику. Попробуйте позже.")
            return

        if popular:
            self.formatter.print_popular_searches(popular)
        else:
            print("Пока нет данных о поисках.")

    def show_recent_searches(self):
        """Показать последние запросы"""
        try:
            recent = self.stats.get_recent_searches(5)
        except (MySQLError, PyMongoError):
            print("Не удалось получить статистику. Попробуйте позже.")
            return

        if recent:
            self.formatter.print_recent_searches(recent)
        else:
            print("Пока нет данных о поисках.")

    def run(self):
        """Запуск главного цикла приложения"""
        print("\n Добро пожаловать в Movie Search App  -MierX- !")
        while True:
            self.show_main_menu()
            choice = input("\nВыберите пункт меню (1-5): ").strip()

            if choice == '1':
                self.search_by_keyword()
            elif choice == '2':
                self.search_by_genre_and_year()
            elif choice == '3':
                self.show_popular_searches()
            elif choice == '4':
                self.show_recent_searches()
            elif choice == '5':
                print("\n До свидания! Спасибо за использование Movie Search App  -MierX- !")
                break
            else:
                print(" Неверный выбор! Попробуйте снова.")

    def __del__(self):
        """Закрытие соединений при завершении"""
        try:
            # Корректное закрытие всех сетевых соединений (MySQL и MongoDB).
            # Используем hasattr для предотвращения ошибок, если объект не был создан
            # из-за сбоя подключения в __init__.
            if hasattr(self, 'movie_db'):
                self.movie_db.close()
            if hasattr(self, 'logger'):
                self.logger.close()
            if hasattr(self, 'stats'):
                self.stats.close()
            print("Все подключения успешно закрыты.")
        except Exception:
            print("Предупреждение: возникла ошибка при закрытии соединений.")

if __name__ == "__main__":
    MovieSearchApp().run()