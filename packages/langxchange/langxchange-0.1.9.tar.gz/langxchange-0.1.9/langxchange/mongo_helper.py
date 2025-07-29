import os
import pymongo
import pandas as pd
from pymongo import MongoClient


class MongoHelper:
    def __init__(self, db_name=None, collection_name=None):
        self.uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = db_name or os.getenv("MONGO_DB", "langxchange")
        self.collection_name = collection_name or os.getenv("MONGO_COLLECTION", "documents")

        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
        except Exception as e:
            raise ConnectionError(f"[❌ ERROR] Failed to connect to MongoDB: {e}")

    def insert(self, documents: list):
        try:
            if isinstance(documents, pd.DataFrame):
                documents = documents.to_dict(orient="records")
            result = self.collection.insert_many(documents)
            return result.inserted_ids
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert documents into MongoDB: {e}")

    def query(self, filter_query: dict = {}, projection: dict = None):
        try:
            cursor = self.collection.find(filter_query, projection)
            return pd.DataFrame(list(cursor))
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query MongoDB: {e}")

    def count(self):
        try:
            return self.collection.count_documents({})
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to count documents: {e}")
