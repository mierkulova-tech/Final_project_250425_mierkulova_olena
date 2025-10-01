"""
                  Модуль для получения статистики поисковых запросов
"""

from pymongo import MongoClient
from typing import List, Dict, Any
import os


class LogStats:

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
            #print("Подключение к MongoDB для статистики успешно!")

        except Exception as e:
            print(f" Ошибка MongoDB (Stats): {e}") # Оставляем для отладки
            raise

    def get_popular_searches(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Получает N самых популярных запросов с помощью агрегации MongoDB."""
        try:
            # Агрегация для подсчета частоты запросов
            pipeline = [
                # Шаг 1: Группировка по search_text для подсчета частоты (count)
                {
                    "$group": {
                        "_id": "$search_text",
                        "count": {"$sum": 1},
                        "search_type": {"$first": "$search_type"},
                        "last_search": {"$max": "$timestamp"},
                        "total_results": {"$sum": "$results_count"}
                    }
                },
                # Шаг 2: Фильтрация, исключающая пустые строки и запросы с 0 счетчиком
                {
                    "$match": {
                        "_id": {"$ne": ""},
                        "count": {"$gt": 0}
                    }
                },
                # Шаг 3: Сортировка по убыванию частоты
                {"$sort": {"count": -1}},
                # Шаг 4: Ограничение результата N элементами
                {"$limit": limit}
            ]

            results = list(self.collection.aggregate(pipeline))

            # Форматируем результат
            popular_searches = []
            for result in results:
                popular_searches.append({
                    "search_text": result["_id"],
                    "count": result["count"],
                    "search_type": result["search_type"],
                    "last_search": result["last_search"],
                    "total_results": result["total_results"]
                })

            return popular_searches

        except Exception as e:
            print(f" Ошибка получения популярных запросов: {e}")
            return []

    def get_recent_searches(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            # Получаем последние уникальные запросы
            pipeline = [
                # Исключаем пустые поиски
                {
                    "$match": {
                        "search_text": {"$ne": ""}
                    }
                },
                # Сортируем по времени (убывание)
                {"$sort": {"timestamp": -1}},
                # Группируем по поисковому тексту (убираем дубликаты)
                {
                    "$group": {
                        "_id": "$search_text",
                        "timestamp": {"$first": "$timestamp"},
                        "search_type": {"$first": "$search_type"},
                        "params": {"$first": "$params"},
                        "results_count": {"$first": "$results_count"}
                    }
                },
                # Еще раз сортируем по времени
                {"$sort": {"timestamp": -1}},
                # Ограничиваем количество
                {"$limit": limit}
            ]

            results = list(self.collection.aggregate(pipeline))

            # Форматируем результат
            recent_searches = []
            for result in results:
                recent_searches.append({
                    "search_text": result["_id"],
                    "timestamp": result["timestamp"],
                    "search_type": result["search_type"],
                    "params": result["params"],
                    "results_count": result["results_count"]
                })

            return recent_searches

        except Exception as e:
            print(f" Ошибка получения последних запросов: {e}")
            return []

    def get_empty_search_count(self) -> int:
        try:
            count = self.collection.count_documents({"results_count": 0})
            return count

        except Exception as e:
            print(f" Ошибка подсчета пустых поисков: {e}")
            return 0

    def get_total_searches(self) -> int:
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f" Ошибка подсчета общего количества: {e}")
            return 0

    def test_connection(self) -> bool:
        try:
            # Пробуем выполнить простую операцию
            self.collection.find_one()
            return True
        except Exception:
            return False

    def close(self):
        try:
            if self.client:
                self.client.close()
                print(" Подключение к MongoDB (статистика) закрыто")
        except Exception as e:
            print(f" Ошибка закрытия подключения: {e}")


def test_log_stats():
    try:
        stats = LogStats()
        print(" Тестирование подключения...")
        if stats.test_connection():
            print(" Подключение работает!")
        else:
            print(" Проблемы с подключением!")
            return

        print(f"\n Общее количество поисков: {stats.get_total_searches()}")
        print(f" Поисков без результатов: {stats.get_empty_search_count()}")

        print("\n Популярные запросы:")
        popular = stats.get_popular_searches(3)
        for i, search in enumerate(popular, 1):
            print(f"  {i}. '{search['search_text']}' - {search['count']} раз")

        print("\n Последние запросы:")
        recent = stats.get_recent_searches(3)
        for search in recent:
            print(f"  - '{search['search_text']}' ({search['search_type']})")

        print("\n Статистика по типам:")
        type_stats = stats.get_search_stats_by_type()
        for search_type, count in type_stats.items():
            print(f"  {search_type}: {count}")

        stats.close()
        print("\n Тест статистики завершен!")

    except Exception as e:
        print(f" Ошибка тестирования статистики: {e}")


if __name__ == "__main__":
    test_log_stats()
