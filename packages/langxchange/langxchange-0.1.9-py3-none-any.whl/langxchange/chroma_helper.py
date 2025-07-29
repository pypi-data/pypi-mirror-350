import os
import uuid
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import chromadb
from chromadb.config import Settings


class ChromaHelper:
    
    def __init__(self, llm_helper, persist_directory=None):
        if not llm_helper or not hasattr(llm_helper, "get_embedding"):
            raise ValueError("❌ A valid LLM helper instance with a 'get_embedding' method is required.")

        self.llm_helper = llm_helper
        persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_PATH", "./chroma_store")
        self.client = chromadb.PersistentClient(path = persist_directory)

    def embed_texts_batched(self, texts: list) -> list:
        return [self.llm_helper.get_embedding(text) for text in texts]

    def ingest_to_chroma(self, df: pd.DataFrame, collection_name: str, engine: str = "llm"):
        batch_size = int(os.getenv("CHROMA_BATCH_SIZE", 100))
        max_workers = int(os.getenv("CHROMA_THREADS", 10))

        collection = self.client.get_or_create_collection(name=collection_name)
        total_records = len(df)
        print(f"🚀 Ingesting {total_records} records into collection '{collection_name}' using engine '{engine}'")

        def process_batch(batch_df):
            texts = batch_df["documents"].tolist()
            ids = [str(uuid.uuid4()) for _ in texts]
            metadatas = batch_df.to_dict(orient="records")

            try:
                embeddings = self.embed_texts_batched(texts)
                collection.add(
                    ids=ids,
                    documents=texts,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                return len(batch_df)
            except Exception as e:
                print(f"❌ Failed to add batch: {e}")
                return 0

        batches = [df[i:i + batch_size] for i in range(0, total_records, batch_size)]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_batch, batch) for batch in batches]
            with tqdm(total=len(batches), desc="🔄 Ingesting", unit="batch") as pbar:
                for future in as_completed(futures):
                    future.result()
                    pbar.update(1)

        return len(collection.get()["ids"])
    
    # def insertone(
    #     self,
    #     df: pd.DataFrame,
    #     collection_name: str
    # ) -> int:
    #     """
    #     Inserts rows of a DataFrame into a Chroma collection.
    #     Expects df to have columns:
    #       - "documents": List[str]
    #       - "metadata": List[dict]
    #     Optionally:
    #       - "embeddings": List[List[float]]  (if present, used directly)
    #     Returns the new total count of items in the collection.
    #     """
    #     collection = self.client.get_or_create_collection(name=collection_name)

    #     texts     = df["documents"].tolist()
    #     metadatas = df["metadata"].tolist()
    #     ids       = [str(uuid.uuid4()) for _ in texts]

    #     # Use provided embeddings if present, else compute
    #     if "embeddings" in df.columns:
    #         embeddings = df["embeddings"].tolist()
    #     else:
    #         embeddings = self.embed_texts_batched(texts)

    #     try:
    #         collection.add(
    #             ids=ids,
    #             documents=texts,
    #             embeddings=embeddings,
    #             metadatas=metadatas
    #         )
    #     except Exception as e:
    #         raise RuntimeError(f"[❌ ERROR] Failed to insert into Chroma: {e}")

    #     return len(collection.get()["ids"])
    def insertone(
        self,
        df: pd.DataFrame,
        collection_name: str
    ) -> int:
        """
        Inserts rows of a DataFrame into a Chroma collection.
        Expects df columns:
          - "documents": List[str]
          - "metadata":  List[dict]
          - "embeddings": List[List[float]]
        Drops any row whose embeddings are not a non-empty list.
        Returns the total count in the collection afterwards.
        """
        collection = self.client.get_or_create_collection(name=collection_name)

        # Validate and filter embeddings
        valid_mask = df["embeddings"].apply(
            lambda emb: isinstance(emb, (list, tuple)) and len(emb) > 0
        )
        if not valid_mask.all():
            skipped = (~valid_mask).sum()
            print(f"⚠️  Skipping {skipped} rows with invalid embeddings")
            df = df[valid_mask].reset_index(drop=True)

        texts     = df["documents"].tolist()
        metadatas = df["metadata"].tolist()
        embeddings= df["embeddings"].tolist()
        ids       = [str(uuid.uuid4()) for _ in texts]

        try:
            collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into Chroma: {e}")

        return len(collection.get()["ids"])
    

    def insert(self, collection_name: str, documents: list, embeddings: list, metadatas: list = None, ids: list = None):
        collection = self.client.get_or_create_collection(name=collection_name)
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{"default": "value"} for _ in documents]
        else:
            metadatas = [{"default": "value", **md} if not md else md for md in metadatas]

        try:
            collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into Chroma: {e}")
        return ids

    # def query(self, collection_name: str, embedding_vector: list, top_k: int = 5, include_metadata: bool = True):
    #     collection = self.client.get_or_create_collection(name=collection_name)
    #     try:
    #         return collection.query(
    #             query_embeddings=[embedding_vector],
    #             n_results=top_k,
    #             include=["documents", "metadatas"] if include_metadata else ["documents"]
    #         )
    #     except Exception as e:
    #         raise RuntimeError(f"[❌ ERROR] Failed to query Chroma: {e}")
    
    def query(self, collection_name: str, embedding_vector: list, top_k: int = 5, include_metadata: bool = True):
        collection = self.client.get_or_create_collection(name=collection_name)
        try:
            return collection.query(
                query_embeddings=[embedding_vector],
                n_results=top_k,
                include=["documents", "metadatas"] if include_metadata else ["documents"]
            )
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query Chroma: {e}")

    def get_collection_count(self, collection_name: str):
        collection = self.client.get_or_create_collection(name=collection_name)
        try:
            return len(collection.get()["ids"])
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Could not get Chroma collection count: {e}")