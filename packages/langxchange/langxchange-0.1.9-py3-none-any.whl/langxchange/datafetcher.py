import pandas as pd

class DataFetcher:
    def __init__(self):
        self.data = None

    # SQLAlchemy (MySQL/PostgreSQL)
    def fetch_from_sqlalchemy(self, engine, query: str):
        try:
            self.data = pd.read_sql(query, engine)
            return self.data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch from SQLAlchemy engine: {e}")

    # SQLite
    def fetch_from_sqlite(self, conn, query: str):
        try:
            self.data = pd.read_sql_query(query, conn)
            conn.close()
            return self.data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch from SQLite: {e}")

    # MongoDB
    def fetch_from_mongodb(self, client, db_name: str, collection_name: str, query: dict = {}):
        try:
            collection = client[db_name][collection_name]
            self.data = pd.DataFrame(list(collection.find(query)))
            return self.data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch from MongoDB: {e}")

    # ChromaDB
    def query_chroma(self, collection, embedding_vector: list, top_k: int = 5, include_metadata: bool = True):
        try:
            results = collection.query(
                query_embeddings=[embedding_vector],
                n_results=top_k,
                include=["documents", "metadatas"] if include_metadata else ["documents"]
            )
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query Chroma: {e}")

    # Pinecone
    def query_pinecone(self, index, embedding_vector: list, top_k: int = 5, include_metadata: bool = True, namespace: str = ""):
        try:
            results = index.query(
                vector=embedding_vector,
                top_k=top_k,
                include_metadata=include_metadata,
                namespace=namespace
            )
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query Pinecone: {e}")
    # CSV
    def fetch_from_csv(self, file_path: str):
        try:
            self.data = pd.read_csv(file_path)
            return self.data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch from CSV: {e}")    
    # JSON
    def fetch_from_json(self, file_path: str):
        try:
            self.data = pd.read_json(file_path)
            return self.data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch from JSON: {e}")