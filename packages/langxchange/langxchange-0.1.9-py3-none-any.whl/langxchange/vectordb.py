import os
import uuid
import chromadb
import pinecone

class VectorDBHelper:
    def __init__(self, engine="chroma", **kwargs):
        self.engine = engine.lower()
        if self.engine == "chroma":
            self.client = chromadb.Client()
            self.collection_name = kwargs.get("collection_name", "langxchange_collection")
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
        elif self.engine == "pinecone":
            api_key = kwargs.get("api_key") or os.getenv("PINECONE_API_KEY")
            environment = kwargs.get("environment") or os.getenv("PINECONE_ENVIRONMENT")
            index_name = kwargs.get("index_name", "langxchange-index")

            pinecone.init(api_key=api_key, environment=environment)
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(index_name, dimension=kwargs.get("dimension", 384))
            self.index = pinecone.Index(index_name)
        else:
            raise ValueError(f"Unsupported vector DB engine: {self.engine}")

    def push(self, vectors, documents, metadatas=None):
        if self.engine == "chroma":
            ids = [str(uuid.uuid4()) for _ in documents]
            self.collection.add(
                documents=documents,
                embeddings=vectors,
                metadatas=metadatas or [{} for _ in documents],
                ids=ids
            )
        elif self.engine == "pinecone":
            ids = [str(uuid.uuid4()) for _ in documents]
            records = list(zip(ids, vectors, metadatas or [{} for _ in documents]))
            self.index.upsert(records)
        else:
            raise RuntimeError("No valid vector DB engine initialized")
