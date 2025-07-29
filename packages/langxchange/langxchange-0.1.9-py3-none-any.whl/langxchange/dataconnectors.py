import os
import pymongo
import sqlite3
from sqlalchemy import create_engine
import chromadb
from chromadb.config import Settings
import pinecone


class DataConnector:
    def __init__(self):
        pass

    # Relational DBs
    def mysql_engine(self):
        url = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
        return create_engine(url)

    def postgres_engine(self):
        url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
        return create_engine(url)

    def sqlite_connection(self):
        return sqlite3.connect(os.getenv("SQLITE_PATH"))

    # NoSQL
    def mongodb_client(self):
        return pymongo.MongoClient(os.getenv("MONGO_URI"))

    # Vector DBs
    def chroma_client(self, collection_name="langxchange_collection"):
        persist_path = os.getenv("CHROMA_PERSIST_PATH", "./chroma_storage")
        client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_path))
        collection = client.get_or_create_collection(name=collection_name)
        return collection

    def pinecone_index(self, dimension=384):
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENVIRONMENT")
        index_name = os.getenv("PINECONE_INDEX", "langxchange-index")

        pinecone.init(api_key=api_key, environment=environment)

        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=dimension)

        return pinecone.Index(index_name)
