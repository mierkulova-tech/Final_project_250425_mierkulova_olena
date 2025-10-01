"""
                  Модуль для получения статистики поисковых запросов
"""

from pymongo import MongoClient
from typing import List, Dict, Any
from datetime import datetime
import os


class LogStats:
    """Класс для работы со статистикой поисковых запросов из MongoDB"""
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        """Подключение к MongoDB через параметры из .env"""
        try:
            mongodb_uri = os.getenv('MONGO_URI')
            database_name = os.getenv('MONGO_DATABASE')
            collection_name = os.getenv('MONGO_COLLECTION')

            self.client = MongoClient(mongodb_uri)
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]

            self.client.server_info()  # проверка подключения
        except Exception as e:
            print(f" Ошибка MongoDB (Stats): {e}")  # Оставляем для отладки
            raise

    def get_recent_searches(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Возвращает последние уникальные поисковые запросы.
        - Исключает пустые поиски
        - Убирает дубликаты
        - Сортирует по времени (от новых к старым)
        - Ограничивает количество
        """
        try:
            pipeline = [
                {"$match": {"search_text": {"$ne": ""}}},  # убираем пустые поиски
                {"$sort": {"timestamp": -1}},  # сортируем по времени
                {
                    "$group": {  # убираем дубликаты
                        "_id": "$search_text",
                        "timestamp": {"$first": "$timestamp"},
                        "search_type": {"$first": "$search_type"},
                        "params": {"$first": "$params"},
                        "results_count": {"$first": "$results_count"}
                    }
                },
                {"$sort": {"timestamp": -1}},  # снова сортируем
                {"$limit": limit}  # ограничиваем количество
            ]

            results = list(self.collection.aggregate(pipeline))

            # Форматируем результат
            recent_searches = [
                {
                    "search_text": result["_id"],
                    "timestamp": result["timestamp"],
                    "search_type": result["search_type"],
                    "params": result["params"],
                    "results_count": result["results_count"]
                }
                for result in results
            ]

            return recent_searches

        except Exception as e:
            print(f" Ошибка получения последних запросов: {e}")
            return []

    def get_popular_searches(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Возвращает самые популярные поисковые запросы (по количеству повторов),
        учитывает ключевые слова и поиск по жанру/годам
        """
        try:
            pipeline = [
                {"$group": {
                    "_id": "$search_text",
                    "count": {"$sum": 1},
                    "search_type": {"$first": "$search_type"},
                    "total_results": {"$sum": "$results_count"},
                    "last_search": {"$max": "$timestamp"}
                }},
                {"$sort": {"count": -1, "last_search": -1}},
                {"$limit": limit}
            ]

            result = list(self.collection.aggregate(pipeline))

            # Преобразуем _id в search_text для удобства вывода
            for item in result:
                item["search_text"] = item.pop("_id")

            return result

        except Exception as e:
            print(f"Ошибка получения популярных поисков: {e}")
            return []

    def get_total_searches_count(self) -> int:
        """Общее количество поисковых запросов."""
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Ошибка подсчета всех логов: {e}")
            return 0

    def get_keyword_searches_count(self) -> int:
        """Количество поисков по ключевым словам."""
        try:
            return self.collection.count_documents({"search_type": "keyword"})
        except Exception as e:
            print(f"Ошибка подсчета поисков по ключевым словам: {e}")
            return 0

    def get_genre_searches_count(self) -> int:
        """
        Количество поисков по жанру и годам.
        """
        try:
            return self.collection.count_documents({"search_type": "genre_year"})
        except Exception as e:
            print(f"Ошибка подсчета поисков по жанру и годам: {e}")
            return 0

    def get_empty_results_count(self) -> int:
        """Количество поисков, которые не дали результатов"""
        try:
            return self.collection.count_documents({"results_count": 0})
        except Exception as e:
            print(f"Ошибка подсчета пустых результатов: {e}")
            return 0

    def close(self):
        """Закрытие подключения к MongoDB"""
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            print(f"Ошибка закрытия подключения: {e}")