"""
                Модуль для записи поисковых запросов в MongoDB
"""


from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any
import os


class LogWriter:

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        try:
            # Чтение из .env
            mongodb_uri = os.getenv('MONGO_URI')
            database_name = os.getenv('MONGO_DATABASE')
            collection_name = os.getenv('MONGO_COLLECTION')

            self.client = MongoClient(mongodb_uri)
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]

            self.client.server_info()
            #print(" Подключение к MongoDB успешно!")

        except Exception as e:
            print(f" Ошибка подключения к MongoDB: {e}") # Оставляем для отладки
            print("Убедитесь, что MongoDB запущен и доступен!")
            raise

    def log_search(self, search_type: str, params: Dict[str, Any], results_count: int):
        try:
            # --- ОПТИМИЗАЦИЯ: Получаем текущее время только один раз ---
            current_time = datetime.now()
        log_entry = {
            "timestamp": current_time,
            "search_type": search_type,
            "params": params,
            "results_count": results_count,

            # Дополнительные поля для статистики (используем сохраненное время)
            "date": current_time.strftime("%Y-%m-%d"),
            "hour": current_time.hour
        }

        # Создаем стандартизированное поле "search_text" для упрощения группировки
            # популярных запросов в LogStats.
            if search_type == "keyword":
                log_entry["search_text"] = params.get("keyword", "").lower()
            elif search_type == "genre_year":
                log_entry[
                    "search_text"] = f"{params.get('genre', '')} {params.get('year_from', '')}-{params.get('year_to', '')}".lower()

            result = self.collection.insert_one(log_entry)

            if result.inserted_id:
                #print(f" Запрос записан в лог (ID: {result.inserted_id})")
                pass
            else:
                print("Не удалось записать лог") # Оставляем предупреждение
        except Exception:
        # Это сообщение помогает в отладке, но не показывается пользователю в main.py
        print(f" Ошибка записи лога ")

    def log_keyword_search(self, keyword: str, results_count: int):
        params = {"keyword": keyword}
        self.log_search("keyword", params, results_count)

    def log_genre_year_search(self, genre: str, year_from: int, year_to: int, results_count: int):
        params = {
            "genre": genre,
            "year_from": year_from,
            "year_to": year_to
        }
        self.log_search("genre_year", params, results_count)

    def get_logs_count(self) -> int:
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f" Ошибка подсчета логов: {e}")
            return 0

    def clear_logs(self) -> bool:
        try:
            result = self.collection.delete_many({})
            print(f"🗑 Удалено записей: {result.deleted_count}")
            return True
        except Exception as e:
            print(f" Ошибка очистки логов: {e}")
            return False

    def get_logs_by_date(self, date: str) -> list:
        try:
            logs = self.collection.find({"date": date}).sort("timestamp", -1)
            return list(logs)
        except Exception as e:
            print(f" Ошибка получения логов по дате: {e}")
            return []

    def get_logs_by_type(self, search_type: str) -> list:
        try:
            logs = self.collection.find({"search_type": search_type}).sort("timestamp", -1)
            return list(logs)
        except Exception as e:
            print(f" Ошибка получения логов по типу: {e}")
            return []

    def test_connection(self) -> bool:
        try:
            self.client.server_info()  # Если сервер недоступен — выбросит исключение
            # Можно также проверить коллекцию на существование
            if self.collection.name:
                return True
            else:
                print(" Коллекция не выбрана")
                return False
        except Exception as e:
            print(f" Ошибка тестирования подключения: {e}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        try:
            stats = {}

            stats['total_logs'] = self.collection.count_documents({})

            keyword_count = self.collection.count_documents({"search_type": "keyword"})
            genre_count = self.collection.count_documents({"search_type": "genre_year"})

            stats['keyword_searches'] = keyword_count
            stats['genre_searches'] = genre_count

            empty_results = self.collection.count_documents({"results_count": 0})
            stats['empty_results'] = empty_results

            return stats

        except Exception as e:
            print(f" Ошибка получения статистики коллекции: {e}")
            return {}

    def close(self):
        try:
            if self.client:
                self.client.close()
                print(" Подключение к MongoDB закрыто")
        except Exception as e:
            print(f" Ошибка закрытия подключения: {e}")


def test_log_writer():
    try:
        logger = LogWriter()

        # Шаг 1: Проверка подключения.
        # Если не работает, тест немедленно завершится, и main.py увидит ошибку.
        if not logger.test_connection():
            print(" Проблемы с подключением к MongoDB!")
            return

        print(" Тест: Запись логов (LogWriter) - Начинаем...")

        # Шаг 2: Тестирование записи логов
        initial_count = logger.get_logs_count()

        # 1. Логируем поиск по ключевому слову
        logger.log_keyword_search("alien", 5)

        # 2. Логируем поиск по жанру/годам
        logger.log_genre_year_search("Action", 2005, 2015, 10)

        final_count = logger.get_logs_count()

        # Шаг 3: Проверка, что лог-записи были добавлены
        if final_count > initial_count:
            print(f" Успех: Добавлено {final_count - initial_count} лог(ов). Запись работает.")
        else:
            print(" Ошибка: Логи не были добавлены в коллекцию.")

        logger.close()

    except Exception as e:
        print(f" Критическая ошибка при тестировании LogWriter: {e}")


if __name__ == "__main__":
    test_log_writer()