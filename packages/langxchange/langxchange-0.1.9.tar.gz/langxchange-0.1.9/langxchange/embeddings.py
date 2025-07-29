# langxchange/embedding_helper.py

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import List, Optional, Union

from sentence_transformers import SentenceTransformer


class EmbeddingHelper:
    """
    High-throughput embedding generator using a provided LLM or SentenceTransformer.
    """

    def __init__(
        self,
        llm,
        batch_size: Optional[int] = None,
        max_workers: Optional[int] = None
    ):
        """
        :param llm: An object with a `.get_embedding(text: str) -> List[float]` method,
                    or a SentenceTransformer instance.
        :param batch_size: Number of texts per batch (default from EMB_BATCH_SIZE or 32)
        :param max_workers: Number of threads for concurrency (default = os.cpu_count())
        """
        self.batch_size = batch_size or int(os.getenv("EMB_BATCH_SIZE", 32))
        self.max_workers = max_workers or (os.cpu_count() or 4)

        if not hasattr(llm, "get_embedding") and not hasattr(llm, "encode"):
            raise ValueError("`llm` must implement `get_embedding(text)` or be a SentenceTransformer.")
        self.client = llm
        self.model = getattr(llm, "__class__", type(llm)).__name__

    def embed(self, texts: List[str]) -> List[Union[List[float], None]]:
        """
        Generate embeddings for a list of texts in parallel batches.
        Returns a list of embedding vectors or None on failure.
        """
        total = len(texts)
        batches = [
            texts[i : i + self.batch_size]
            for i in range(0, total, self.batch_size)
        ]

        embeddings: List[Optional[List[float]]] = [None] * total

        with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            futures = {}
            idx = 0
            for batch in batches:
                futures[exe.submit(self._embed_batch, batch)] = (idx, len(batch))
                idx += len(batch)

            for fut in tqdm(as_completed(futures), total=len(futures), desc="Embedding"):
                start, length = futures[fut]
                try:
                    result = fut.result()
                except Exception:
                    result = [None] * length
                embeddings[start : start + length] = result

        return embeddings
    
    # def _embed_batch(self, batch: List[str]) -> List[List[float]]:
    #     # Otherwise assume SentenceTransformer
    #     emb = self.client.encode(batch, convert_to_numpy=False, show_progress_bar=False)
    #     # Otherwise assume SentenceTransformer – coerce every item to str
    #     batch_strs = [str(item) for item in batch]
    #     emb = self.client.encode(
    #         batch_strs,
    #        convert_to_numpy=False,
    #         show_progress_bar=False
    #     )
    #     return [e.tolist() if hasattr(e, "tolist") else e for e in emb]
    def _embed_batch(self, batch: List[str]) -> List[List[float]]:
        """
        Dispatch a batch to the underlying client.
        """
        # If client supports get_embedding
        if hasattr(self.client, "get_embedding"):
            return [self.client.get_embedding(text) for text in batch]

        # Otherwise assume SentenceTransformer
        emb = self.client.encode(batch, convert_to_numpy=False, show_progress_bar=False)
        return [e.tolist() if hasattr(e, "tolist") else e for e in emb]
