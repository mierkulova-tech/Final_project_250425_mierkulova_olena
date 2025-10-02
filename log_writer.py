"""
                Модуль для записи поисковых запросов в MongoDB
"""


from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any
import os


class LogWriter:
    """Простое логирование поисковых запросов в MongoDB."""
    def __init__(self):
        self.client = None
        self.collection = None
        self.connect()

    def connect(self):
        """Подключение к MongoDB."""
        # Чтение из .env
        mongodb_uri = os.getenv('MONGO_URI')
        database_name = os.getenv('MONGO_DATABASE')
        collection_name = os.getenv('MONGO_COLLECTION')

        self.client = MongoClient(mongodb_uri)
        self.collection = self.client[database_name][collection_name]
        # Проверка соединения
        self.client.server_info()

    def log_search(self, search_type: str, params: Dict[str, Any], results_count: int, search_text=None):
        """Запись одного поиска в коллекцию."""
        log_entry = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "search_text": search_text,
            "params": params,
            "results_count": results_count
        }
        self.collection.insert_one(log_entry)

    def log_keyword_search(self, keyword: str, results_count: int):
        params = {"keyword": keyword}
        search_text = keyword  # для статистики
        self.log_search("keyword", params, results_count,  search_text)

    def log_genre_year_search(self, genre: str, year_from: int, year_to: int, results_count: int):
        params = {"genre": genre,"year_from": year_from,"year_to": year_to}
        search_text = f"{genre} ({year_from}-{year_to})"  # для статистики
        self.log_search("genre_year", params, results_count, search_text)



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
        except Exception as e:
            print(f" Ошибка закрытия подключения: {e}")