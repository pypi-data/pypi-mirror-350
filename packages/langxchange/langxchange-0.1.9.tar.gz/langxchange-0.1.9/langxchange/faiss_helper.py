# langxchange/faiss_helper.py

import os
import uuid
import pickle
import numpy as np
import faiss
import pandas as pd
from typing import List, Dict, Any, Optional


class FAISSHelper:
    """
    FAISS-based vector store with in-memory metadata and optional persistence.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata_store: Dict[str, Dict[str, Any]] = {}
        self.id_list: List[str] = []

    def insert(
        self,
        vectors: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        arr = np.asarray(vectors, dtype="float32")
        if arr.ndim != 2 or arr.shape[1] != self.dim:
            raise ValueError(f"Invalid vectors shape {arr.shape}, expected (n, {self.dim})")
        self.index.add(arr)

        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{} for _ in documents]

        for _id, doc, meta in zip(ids, documents, metadatas):
            self.metadata_store[_id] = {"text": doc, "metadata": meta}
            self.id_list.append(_id)

        return ids

    def insertone(self, df: pd.DataFrame) -> int:
        def valid_emb(e):
            try:
                arr = np.asarray(e, dtype="float32")
                return arr.ndim == 1 and arr.shape[0] == self.dim
            except Exception:
                return False

        valid_mask = df["embeddings"].apply(valid_emb)
        if not valid_mask.all():
            skipped = (~valid_mask).sum()
            print(f"⚠️  Skipping {skipped} rows with invalid embeddings")
            df = df[valid_mask].reset_index(drop=True)

        documents = df["documents"].tolist()
        metadatas = df["metadata"].tolist()
        embeddings = [np.asarray(e, dtype="float32") for e in df["embeddings"].tolist()]
        arr = np.stack(embeddings, axis=0)
        self.index.add(arr)

        for _id, doc, meta in zip([str(uuid.uuid4()) for _ in documents], documents, metadatas):
            self.metadata_store[_id] = {"text": doc, "metadata": meta}
            self.id_list.append(_id)

        return int(self.index.ntotal)

    def query(self, embedding_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        if self.index.ntotal == 0:
            return []

        arr = np.asarray(embedding_vector, dtype="float32")
        if arr.ndim == 1:
            vec = arr.reshape(1, -1)
        elif arr.ndim == 2 and arr.shape == (1, self.dim):
            vec = arr
        else:
            raise ValueError(f"Invalid embedding_vector shape {arr.shape}, expected 1D of length {self.dim} or shape (1, {self.dim})")

        try:
            result = self.index.search(vec, top_k)
            if isinstance(result, tuple) and len(result) == 2:
                _, I = result
            else:
                raise RuntimeError(f"Unexpected return from faiss.Index.search: {result!r}")
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query FAISS: {e}")

        hits = []
        for idx in I[0]:
            if 0 <= idx < len(self.id_list):
                _id = self.id_list[idx]
                entry = self.metadata_store[_id]
                hits.append({
                    "id": _id,
                    "text": entry["text"],
                    "metadata": entry["metadata"]
                })
        return hits

    def count(self) -> int:
        return int(self.index.ntotal)

    # ─── Persistence Methods ────────────────────────────────────────────────────

    def save(self, index_path: str, metadata_path: Optional[str] = None):
        faiss.write_index(self.index, index_path)
        meta_file = metadata_path or index_path + ".meta"
        with open(meta_file, "wb") as f:
            pickle.dump({
                "id_list": self.id_list,
                "metadata_store": self.metadata_store,
                "dim": self.dim
            }, f)

    def load(self, index_path: str, metadata_path: Optional[str] = None):
        # 1) Load FAISS index
        if not os.path.isfile(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")
        self.index = faiss.read_index(index_path)

        # 2) Load metadata
        meta_file = metadata_path or f"{index_path}.meta"
        if not os.path.isfile(meta_file):
            raise FileNotFoundError(f"Metadata file not found: {meta_file}")
        with open(meta_file, "rb") as f:
            data = pickle.load(f)

        # 3) Override helper.dim to match persisted index
        stored_dim = data.get("dim")
        if stored_dim is None:
            raise RuntimeError(f"'dim' not found in metadata file: {meta_file}")
        self.dim = stored_dim

        # 4) Restore IDs & metadata
        self.id_list = data.get("id_list", [])
        self.metadata_store = data.get("metadata_store", {})

    def clear(self):
        self.index.reset()
        self.metadata_store.clear()
        self.id_list.clear()

    def delete_persistence(self, index_path: str, metadata_path: Optional[str] = None):
        for path in [index_path, metadata_path or f"{index_path}.meta"]:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


# # langxchange/faiss_helper.py

# import os
# import uuid
# import pickle
# import numpy as np
# import faiss
# import pandas as pd
# from typing import List, Dict, Any, Optional


# class FAISSHelper:
#     """
#     FAISS-based vector store with in-memory metadata and optional persistence.
#     """

#     def __init__(self, dim: int = 384):
#         self.dim = dim
#         self.index = faiss.IndexFlatL2(dim)
#         self.metadata_store: Dict[str, Dict[str, Any]] = {}
#         self.id_list: List[str] = []

#     def insert(
#         self,
#         vectors: List[List[float]],
#         documents: List[str],
#         metadatas: Optional[List[Dict[str, Any]]] = None,
#         ids: Optional[List[str]] = None
#     ) -> List[str]:
#         # ... existing insert implementation ...
#         arr = np.asarray(vectors, dtype="float32")
#         if arr.ndim != 2 or arr.shape[1] != self.dim:
#             raise ValueError(f"Invalid vectors shape {arr.shape}, expected (n, {self.dim})")
#         self.index.add(arr)
#         if not ids:
#             ids = [str(uuid.uuid4()) for _ in documents]
#         if not metadatas:
#             metadatas = [{} for _ in documents]
#         for _id, doc, meta in zip(ids, documents, metadatas):
#             self.metadata_store[_id] = {"text": doc, "metadata": meta}
#             self.id_list.append(_id)
#         return ids

#     def insertone(self, df: pd.DataFrame) -> int:
#         # ... existing insertone implementation ...
#         def valid_emb(e):
#             try:
#                 arr = np.asarray(e, dtype="float32")
#                 return arr.ndim == 1 and arr.shape[0] == self.dim
#             except Exception:
#                 return False

#         valid_mask = df["embeddings"].apply(valid_emb)
#         if not valid_mask.all():
#             skipped = (~valid_mask).sum()
#             print(f"⚠️  Skipping {skipped} rows with invalid embeddings")
#             df = df[valid_mask].reset_index(drop=True)

#         documents = df["documents"].tolist()
#         metadatas = df["metadata"].tolist()
#         embeddings = [np.asarray(e, dtype="float32") for e in df["embeddings"].tolist()]
#         arr = np.stack(embeddings, axis=0)
#         self.index.add(arr)
#         for _id, doc, meta in zip([str(uuid.uuid4()) for _ in documents], documents, metadatas):
#             self.metadata_store[_id] = {"text": doc, "metadata": meta}
#             self.id_list.append(_id)
#         return int(self.index.ntotal)

#     def query(self, embedding_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
#         # ... existing query implementation ...
#         if self.index.ntotal == 0:
#             return []
#         arr = np.asarray(embedding_vector, dtype="float32")
#         if arr.ndim == 1:
#             vec = arr.reshape(1, -1)
#         elif arr.ndim == 2 and arr.shape == (1, self.dim):
#             vec = arr
#         else:
#             raise ValueError(f"Invalid embedding_vector shape {arr.shape}, expected (dim,) or (1, dim)")
#         result = self.index.search(vec, top_k)
#         if not (isinstance(result, tuple) and len(result) == 2):
#             raise RuntimeError(f"Unexpected FAISS return: {result!r}")
#         D, I = result
#         hits = []
#         for idx in I[0]:
#             if 0 <= idx < len(self.id_list):
#                 _id = self.id_list[idx]
#                 entry = self.metadata_store[_id]
#                 hits.append({
#                     "id": _id,
#                     "text": entry["text"],
#                     "metadata": entry["metadata"]
#                 })
#         return hits

#     def count(self) -> int:
#         return int(self.index.ntotal)

#     # ─── Persistence Methods ────────────────────────────────────────────────────

#     def save(self, index_path: str, metadata_path: Optional[str] = None):
#         """
#         Persist FAISS index and metadata to disk.
#         """
#         faiss.write_index(self.index, index_path)
#         meta_file = metadata_path or index_path + ".meta"
#         with open(meta_file, "wb") as f:
#             pickle.dump({
#                 "id_list": self.id_list,
#                 "metadata_store": self.metadata_store,
#                 "dim": self.dim
#             }, f)

#     def load(self, index_path: str, metadata_path: Optional[str] = None):
#         """
#         Load FAISS index and metadata from disk.
#         """
#         if not os.path.isfile(index_path):
#             raise FileNotFoundError(f"Index file not found: {index_path}")
#         self.index = faiss.read_index(index_path)
#         meta_file = metadata_path or index_path + ".meta"
#         if not os.path.isfile(meta_file):
#             raise FileNotFoundError(f"Metadata file not found: {meta_file}")
#         with open(meta_file, "rb") as f:
#             data = pickle.load(f)
#         if data.get("dim") != self.dim:
#             raise RuntimeError(f"Dimension mismatch: index dim={data.get('dim')} vs helper dim={self.dim}")
#         self.id_list = data["id_list"]
#         self.metadata_store = data["metadata_store"]

#     def clear(self):
#         """
#         Clear in-memory index and metadata (does not delete disk files).
#         """
#         self.index.reset()
#         self.metadata_store.clear()
#         self.id_list.clear()

#     def delete_persistence(self, index_path: str, metadata_path: Optional[str] = None):
#         """
#         Delete persisted index and metadata files from disk.
#         """
#         for path in [index_path, metadata_path or index_path + ".meta"]:
#             try:
#                 os.remove(path)
#             except FileNotFoundError:
#                 pass
