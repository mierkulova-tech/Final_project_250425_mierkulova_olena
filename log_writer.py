"""
Модуль для записи поисковых запросов в MongoDB
"""

import os
from pymongo import MongoClient
from datetime import datetime, timezone
from typing import Dict, Any
from dotenv import load_dotenv


class LogWriter:
    """
    Класс для записи и управления логами поисковых запросов в MongoDB.
    """

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        """
        Подключение к MongoDB и выбор коллекции.
        """
        load_dotenv()

        mongodb_uri = os.getenv(
            "MONGODB_URI",
            "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
        )
        database_name = os.getenv("MONGODB_DB", "ich_edit")
        collection_name = os.getenv("MONGODB_COLLECTION", "Final_project_250425_mierkulova_olena")

        self.client = MongoClient(mongodb_uri)
        self.client.server_info()
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def log_search(self, search_type: str, params: Dict[str, Any], results_count: int) -> str:
        """
        Записывает поисковый запрос в коллекцию.
        """
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        log_entry = {
            "date": today,
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }

        if search_type == "keyword":
            log_entry["search_text"] = params.get("keyword", "").lower()
        elif search_type == "genre_year":
            log_entry["search_text"] = f"{params.get('genre', '')} {params.get('year_from', '')}-{params.get('year_to', '')}".lower()

        result = self.collection.insert_one(log_entry)
        return str(result.inserted_id)

    def log_keyword_search(self, keyword: str, results_count: int) -> str:
        """
        Логирует поиск по ключевому слову.
        """
        params = {"keyword": keyword}
        return self.log_search("keyword", params, results_count)

    def log_genre_year_search(self, genre: str, year_from: int, year_to: int, results_count: int) -> str:
        """
        Логирует поиск по жанру и годам.
        """
        params = {
            "genre": genre,
            "year_from": year_from,
            "year_to": year_to
        }
        return self.log_search("genre_year", params, results_count)

    def get_logs_by_date(self, date: str) -> list:
        """
        Получает логи по дате.
        """
        logs = self.collection.find({"date": date})
        return list(logs)

    def get_logs_by_type(self, search_type: str) -> list:
        """
        Получает логи по типу поиска.
        """
        logs = self.collection.find({"search_type": search_type})
        return list(logs)

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Получает статистику по коллекции логов.
        """
        stats = {
            "total_logs": self.collection.count_documents({}),
            "keyword_searches": self.collection.count_documents({"search_type": "keyword"}),
            "genre_searches": self.collection.count_documents({"search_type": "genre_year"}),
            "empty_results": self.collection.count_documents({"results_count": 0})
        }
        return stats

    def close(self):
        """
        Закрывает соединение с MongoDB.
        """
        if self.client:
            self.client.close()
