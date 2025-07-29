import os
import uuid
import numpy as np
from opensearchpy import OpenSearch, helpers


class OpenSearchHelper:
    def __init__(self, index_name="langxchange_index", dim=384):
        self.index_name = index_name
        self.dim = dim
        self.client = OpenSearch(
            hosts=[os.getenv("OS_HOST", "http://localhost:9200")],
            http_auth=(os.getenv("OS_USER", ""), os.getenv("OS_PASSWORD", "")),
            verify_certs=False
        )
        self._init_index()

    def _init_index(self):
        if self.client.indices.exists(index=self.index_name):
            return

        mapping = {
            "settings": {
                "index": {
                    "knn": True
                }
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": self.dim
                    },
                    "metadata": {"type": "object"}
                }
            }
        }

        self.client.indices.create(index=self.index_name, body=mapping)

    def insert(self, vectors: list, documents: list, metadatas: list = None, ids: list = None):
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{} for _ in documents]

        actions = [
            {
                "_index": self.index_name,
                "_id": _id,
                "_source": {
                    "text": doc,
                    "embedding": vec,
                    "metadata": meta
                }
            }
            for _id, doc, vec, meta in zip(ids, documents, vectors, metadatas)
        ]

        try:
            helpers.bulk(self.client, actions)
            return ids
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into OpenSearch: {e}")

    def query(self, embedding_vector: list, top_k: int = 5):
        try:
            query = {
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": embedding_vector,
                            "k": top_k
                        }
                    }
                }
            }
            res = self.client.search(index=self.index_name, body=query)
            return [
                {
                    "text": hit["_source"]["text"],
                    "score": hit["_score"],
                    "metadata": hit["_source"].get("metadata", {})
                }
                for hit in res["hits"]["hits"]
            ]
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query OpenSearch: {e}")
