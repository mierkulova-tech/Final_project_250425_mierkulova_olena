"""
                                            "MierX"

"""

from mysql_connector import MovieDatabase
from log_writer import LogWriter
from log_stats import LogStats
from formatter import ResultFormatter



class MovieSearchApp:
    """
        Основное приложение для поиска фильмов.

        Атрибуты:
            movie_db (MovieDatabase): интерфейс для работы с базой фильмов.
            logger (LogWriter): объект для записи логов.
            stats (LogStats): объект для получения статистики поисков.
            formatter (ResultFormatter): форматирование и вывод результатов.
    """

    def __init__(self):
        """
        Инициализация компонентов приложения.
        """
        self.movie_db = MovieDatabase()
        self.logger = LogWriter()
        self.stats = LogStats()
        self.formatter = ResultFormatter()


    def show_main_menu(self):
        """
        Выводит главное меню приложения.
        """
        print("\n" + "=" * 50)
        print(" MOVIE SEARCH APP  -MierX- ")
        print("=" * 50)
        print("1.  Поиск по ключевому слову")
        print("2.  Поиск по жанру и годам")
        print("3.  Популярные запросы")
        print("4.  Выйти")
        print("=" * 50)

    def search_by_keyword(self):
        """
        Обработка поиска фильмов по ключевому слову с постраничным выводом.
        Логирует первый запрос.
        """
        print("\n ПОИСК ПО КЛЮЧЕВОМУ СЛОВУ")
        print("-" * 30)

        keyword = input("Введите ключевое слово: ").strip().lower()
        if not keyword:
            print(" Ключевое слово не может быть пустым!")
            return


        offset = 0
        while True:
            movies = self.movie_db.search_by_keyword(keyword, offset)

            if not movies:
                if offset == 0:
                    print(f" По запросу '{keyword}' ничего не найдено")
                else:
                    print("Больше результатов нет")
                break

            self.formatter.print_movies(movies)

            if offset == 0:
                self.logger.log_search("keyword", {"keyword": keyword}, len(movies))

            if len(movies) == 10:
                choice = input("\n Показать следующие 10? (y/n): ").lower()
                if choice != 'y':
                    break
                offset += 10
            else:
                break



    def search_by_genre_and_year(self):
        """
        Показывает популярные поисковые запросы.
        """
        print("\n ПОИСК ПО ЖАНРУ И ГОДАМ")
        print("-" * 30)

        genres = self.movie_db.get_all_genres()
        print(" Доступные жанры:")
        self.formatter.print_genres(genres)

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
            year_from = int(input("Год с (например 1990): "))
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



    def show_popular_searches(self):
        """
        Показывает популярные поисковые запросы.
        """
        print("\n ПОПУЛЯРНЫЕ ЗАПРОСЫ")
        print("-" * 30)

        popular = self.stats.get_popular_searches(5)
        if popular:
            self.formatter.print_popular_searches(popular)
        else:
            print(" Пока нет данных о поисках")

    def run(self):
        """
        Запускает главный цикл приложения для взаимодействия с пользователем.
        """
        print("\n Добро пожаловать!")

        while True:
            self.show_main_menu()
            choice = input("\nВыберите пункт меню (1-4): ").strip()

            if choice == '1':
                self.search_by_keyword()
            elif choice == '2':
                self.search_by_genre_and_year()
            elif choice == '3':
                self.show_popular_searches()
            elif choice == '4':
                print("\n До свидания!")
                break
            else:
                print(" Неверный выбор! Попробуйте снова.")

    def close(self):
        """
        Закрывает все ресурсы: БД, логгер, статистику.
        """
        self.movie_db.close()
        self.logger.close()
        self.stats.close()

def main():
        app = MovieSearchApp()
        app.run()

if __name__ == "__main__":
    main()