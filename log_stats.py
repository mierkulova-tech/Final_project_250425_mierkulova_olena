"""
Модуль для получения статистики поисковых запросов
"""

from pymongo import MongoClient
from typing import List, Dict, Any


class LogStats:
    """
    Класс для получения статистики поисковых запросов из MongoDB.
    """

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        mongodb_uri = "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
        database_name = "ich_edit"
        collection_name = "Final_project_250425_mierkulova_olena"

        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def get_popular_searches(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Возвращает список популярных поисковых запросов с их статистикой.
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$search_text",
                    "count": {"$sum": 1},
                    "search_type": {"$first": "$search_type"},
                    "last_search": {"$max": "$date"},
                    "total_results": {"$sum": "$results_count"}
                }
            },
            {"$match": {"_id": {"$ne": ""}, "count": {"$gt": 0}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        results = list(self.collection.aggregate(pipeline))

        # Переименовываем _id в search_text для удобства
        for r in results:
            if "_id" in r:
                r["search_text"] = r.pop("_id")

        return results

    def get_search_stats_by_type(self) -> Dict[str, int]:
        pipeline = [
            {"$group": {"_id": "$search_type", "count": {"$sum": 1}}}
        ]
        results = list(self.collection.aggregate(pipeline))
        stats = {r["_id"]: r["count"] for r in results}
        return stats

    def get_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        pipeline = [
            {
                "$group": {
                    "_id": "$date",
                    "total_searches": {"$sum": 1},
                    "keyword_searches": {
                        "$sum": {"$cond": [{"$eq": ["$search_type", "keyword"]}, 1, 0]}
                    },
                    "genre_searches": {
                        "$sum": {"$cond": [{"$eq": ["$search_type", "genre_year"]}, 1, 0]}
                    }
                }
            },
            {"$sort": {"_id": -1}},
            {"$limit": days}
        ]
        results = list(self.collection.aggregate(pipeline))
        daily_stats = [
            {
                "date": r["_id"],
                "total_searches": r["total_searches"],
                "keyword_searches": r["keyword_searches"],
                "genre_searches": r["genre_searches"]
            }
            for r in results
        ]
        return daily_stats

    def get_empty_search_count(self) -> int:
        return self.collection.count_documents({"results_count": 0})

    def get_total_searches(self) -> int:
        return self.collection.count_documents({})

    def close(self):
        if self.client:
            self.client.close()
