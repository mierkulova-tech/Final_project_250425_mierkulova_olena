"""
                                            "MierX"
                                        Movie Search App
                        Приложение для поиска фильмов с логированием в MongoDB
"""

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

            #print("Подключение к базам данных успешно!")

        except Exception:
            print("Не удалось установить соединение с базой данных.")
            print("Проверьте настройки (.env) и доступность сервера.")
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
        """Поиск фильмов по ключевому слову"""
        print("\n ПОИСК ПО КЛЮЧЕВОМУ СЛОВУ")
        print("-" * 30)

        keyword = input("Введите ключевое слово: ").strip().lower()
        if not keyword:
            print(" Ключевое слово не может быть пустым!")
            return

        try:
            offset = 0
            while True:
                # Поиск фильмов
                movies = self.movie_db.search_by_keyword(keyword, offset)

                if not movies:
                    if offset == 0:
                        print(f" По запросу '{keyword}' ничего не найдено")
                        # Логируем даже пустые результаты
                        self.logger.log_search("keyword", {"keyword": keyword}, 0)
                    else:
                        print(" Больше результатов нет")
                    break

                # Показываем результаты
                print(f"\n Найдено фильмов (показаны {offset + 1}-{offset + len(movies)}):")
                self.formatter.print_movies(movies)

                # Логируем поиск только при первых результатах
                if offset == 0:
                    self.logger.log_search("keyword", {"keyword": keyword}, len(movies))

                # Спрашиваем про продолжение
                if len(movies) == 10:  # Если получили полную страницу
                    choice = input("\n Показать следующие 10? (y/n): ").lower()
                    if choice != 'y':
                        break
                    offset += 10
                else:
                    break

        except Exception as e:
            print(f" Ошибка поиска: {e}")

    def search_by_genre_and_year(self):
        """Поиск фильмов по жанру и диапазону лет"""
        print("\n ПОИСК ПО ЖАНРУ И ГОДАМ")
        print("-" * 30)

        try:
            # Показываем доступные жанры
            genres = self.movie_db.get_all_genres()
            print(" Доступные жанры:")
            self.formatter.print_genres(genres)

            # Показываем диапазон лет
            year_range = self.movie_db.get_year_range()
            print(f"\n Диапазон лет: {year_range['min']} - {year_range['max']}")

            # Запрашиваем жанр
            genre = input("\nВведите жанр: ").strip()
            if not genre:
                print(" Жанр не может быть пустым!")
                return

            # Проверяем, существует ли жанр
            if genre not in [g['name'] for g in genres]:
                print(f" Жанр '{genre}' не найден!")
                return

            # Запрашиваем годы
            try:
                year_from = int(input("Год с (например 2000): "))
                year_to = int(input("Год до (например 2020): "))

                if year_from > year_to:
                    print(" Год 'с' не может быть больше года 'до'!")
                    return

            except ValueError:
                print(" Годы должны быть числами!")
                return

            # Поиск с пагинацией
            offset = 0
            search_params = {
                "genre": genre,
                "year_from": year_from,
                "year_to": year_to
            }

            while True:
                movies = self.movie_db.search_by_genre_and_year(
                    genre, year_from, year_to, offset
                )

                if not movies:
                    if offset == 0:
                        print(f" По запросу не найдено фильмов")
                        self.logger.log_search("genre_year", search_params, 0)
                    else:
                        print(" Больше результатов нет")
                    break

                # Показываем результаты
                print(f"\n Найдено фильмов (показаны {offset + 1}-{offset + len(movies)}):")
                self.formatter.print_movies_with_genre(movies)

                # Логируем только первые результаты
                if offset == 0:
                    self.logger.log_search("genre_year", search_params, len(movies))

                # Проверяем продолжение
                if len(movies) == 10:
                    choice = input("\n Показать следующие 10? (y/n): ").lower()
                    if choice != 'y':
                        break
                    offset += 10
                else:
                    break

        except Exception as e:
            print(f" Ошибка поиска: {e}")

    def show_popular_searches(self):
        """Показать популярные запросы"""
        print("\n ПОПУЛЯРНЫЕ ЗАПРОСЫ")
        print("-" * 30)

        try:
            popular = self.stats.get_popular_searches(5)
            if popular:
                self.formatter.print_popular_searches(popular)
            else:
                print(" Пока нет данных о поисках")

        except Exception as e:
            print(f" Ошибка получения статистики: {e}")

    def show_recent_searches(self):
        """Показать последние запросы"""
        print("\n ПОСЛЕДНИЕ ЗАПРОСЫ")
        print("-" * 30)

        try:
            recent = self.stats.get_recent_searches(5)
            if recent:
                self.formatter.print_recent_searches(recent)
            else:
                print(" Пока нет данных о поисках")

        except Exception as e:
            print(f"Ошибка получения статистики: {e}")

    def run(self):
        """Запуск главного цикла приложения"""
        print("\n Добро пожаловать в Movie Search App  -MierX- !")

        while True:
            try:
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

            except KeyboardInterrupt:
                print("\n\n Программа прервана пользователем. До свидания!")
                break
            except Exception as e:
                print(f" Неожиданная ошибка: {e}")
                print("Попробуйте снова или перезапустите программу  -MierX- .")

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
        except:
            # Игнорируем ошибки при закрытии, чтобы не прерывать завершение программы.
            pass


def main():
    """Главная функция"""
    app = MovieSearchApp()
    app.run()

if __name__ == "__main__":
    main()