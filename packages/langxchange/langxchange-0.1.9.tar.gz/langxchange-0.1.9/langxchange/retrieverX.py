# langxchange/retrieverX.py

from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import CrossEncoder


class RetrieverX:
    """
    Two-stage retrieval: vector search + optional cross-encoder re-ranking.

    :param vector_db: any object with a `.query(...)` method
                      Chroma signature: query(collection_name, embedding_vector, top_k, include_metadata=True)
                      FAISS signature: query(embedding_vector, top_k)
    :param embedder: an object with an `.embed([query]) -> [[float]]` method
    :param reranker_model: name of a CrossEncoder model, e.g. "cross-encoder/ms-marco-MiniLM-L-6-v2"
    :param use_rerank: whether to apply cross-encoder re-ranking
    """

    def __init__(
        self,
        vector_db: Any,
        embedder: Any,
        reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        use_rerank: bool = True
    ):
        self.vector_db = vector_db
        self.embedder = embedder
        self.use_rerank = use_rerank
        self.reranker: Optional[CrossEncoder] = None
        if self.use_rerank:
            self.reranker = CrossEncoder(reranker_model)

    def retrieve(
        self,
        query: str,
        collection_name: str,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform retrieval pipeline.

        :param query: user query string
        :param collection_name: vector DB collection to query (ChromaHelper only)
        :param top_k: number of candidates to return (after reranking if enabled)
        :return: list of {"document": str, "metadata": dict, "score": float}
        """
        # 1) embed the query
        q_emb = self.embedder.embed([query])[0]

        # 2) initial vector DB retrieval
        try:
            if collection_name == None:
                 # Fallback to FAISSHelper signature
                hits = self.vector_db.query(q_emb, top_k * (2 if self.use_rerank else 1))
                docs   = [h.get("text", "")     for h in hits]
                metas  = [h.get("metadata", {}) for h in hits]
                scores = [0.0 for _ in hits]
                res = {"documents": docs, "metadatas": metas, "scores": scores}
                
            else:
               # Try Chroma-like signature
                res = self.vector_db.query(
                    collection_name=collection_name,
                    embedding_vector=q_emb,
                    top_k=top_k * (2 if self.use_rerank else 1),
                    include_metadata=True
                ) 

        except TypeError as e:
           raise RuntimeError(f"[❌ ERROR] Unexpected Error during retrieval : {e}")

        if not isinstance(res, dict):
            raise RuntimeError(f"[❌ ERROR] Vector DB returned invalid response: {res!r}")

        # 3) normalize fields
        docs   = res.get("documents") or []
        metas  = res.get("metadatas") or []
        scores = res.get("distances", res.get("scores", None))

        n = len(docs)
        if len(metas) != n:
            metas = [{}] * n
        if not isinstance(scores, list) or len(scores) != n:
            scores = [0.0] * n

        candidates: List[Tuple[str, Dict[str, Any], float]] = list(zip(docs, metas, scores))

        # 4) optional re-ranking
        if self.use_rerank and self.reranker:
            pairs = [[query, doc] for doc, _, _ in candidates]
            rerank_scores = self.reranker.predict(pairs)
            reranked = sorted(
                zip(candidates, rerank_scores),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
            return [
                {"document": doc, "metadata": meta, "score": float(r_score)}
                for ((doc, meta, _), r_score) in reranked
            ]

        # 5) no rerank: return top_k by original score
        sorted_orig = sorted(candidates, key=lambda x: x[2], reverse=True)[:top_k]
        return [
            {"document": doc, "metadata": meta, "score": float(score)}
            for doc, meta, score in sorted_orig
        ]


# # langxchange/retrieverX.py

# from typing import List, Dict, Any, Optional, Tuple
# from sentence_transformers import CrossEncoder


# class RetrieverX:
#     """
#     Two-stage retrieval: vector search + optional cross-encoder re-ranking.

#     :param vector_db: any object with a `.query(collection_name, embedding_vector, top_k, include_metadata=True)` method
#                       returning a dict with keys "documents" (List[str]), optionally "metadatas", "distances" or "scores".
#     :param embedder: an object with an `.embed([query]) -> [[float]]` method
#     :param reranker_model: name of a CrossEncoder model, e.g. "cross-encoder/ms-marco-MiniLM-L-6-v2"
#     :param use_rerank: whether to apply cross-encoder re-ranking
#     """

#     def __init__(
#         self,
#         vector_db: Any,
#         embedder: Any,
#         reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
#         use_rerank: bool = True
#     ):
#         self.vector_db = vector_db
#         self.embedder = embedder
#         self.use_rerank = use_rerank
#         self.reranker: Optional[CrossEncoder] = None
#         if self.use_rerank:
#             self.reranker = CrossEncoder(reranker_model)

#     def retrieve(
#         self,
#         query: str,
#         collection_name: str,
#         top_k: int = 10
#     ) -> List[Dict[str, Any]]:
#         """
#         Perform retrieval pipeline.

#         :param query: user query string
#         :param collection_name: vector DB collection to query
#         :param top_k: number of candidates to return (after reranking if enabled)
#         :return: list of {"document": str, "metadata": dict, "score": float}
#         """
#         # 1) embed the query
#         q_emb = self.embedder.embed([query])[0]

#         # 2) initial vector DB retrieval
#         res = self.vector_db.query(
#             collection_name=collection_name,
#             embedding_vector=q_emb,
#             top_k=top_k * (2 if self.use_rerank else 1),
#             include_metadata=True
#         )
#         #return res
#         if not isinstance(res, dict):
#             raise RuntimeError(f"[❌ ERROR] Vector DB returned invalid response: {res!r}")

#         docs   = res.get("documents") or []
#         metas  = res.get("metadatas") or []
#         scores = res.get("distances", res.get("scores", None))

#         n = len(docs)
#         if len(metas) != n:
#             metas = [{}] * n
#         if not isinstance(scores, list) or len(scores) != n:
#             scores = [0.0] * n

#         candidates: List[Tuple[str, Dict[str, Any], float]] = list(zip(docs, metas, scores))

#         # 3) optional re-ranking
#         # if self.use_rerank and self.reranker:
#         #     pairs = [[query, doc] for doc, _, _ in candidates]
#         #     rerank_scores = self.reranker.predict(pairs)
#         #     reranked = sorted(
#         #         zip(candidates, rerank_scores),
#         #         key=lambda x: x[1],
#         #         reverse=True
#         #     )[:top_k]
#         #     return [
#         #         {"document": doc, "metadata": meta, "score": float(r_score)}
#         #         for ((doc, meta, _), r_score) in reranked
#         #     ]

#         # 4) no rerank: return top_k by original score
#         sorted_orig = sorted(candidates, key=lambda x: x[2], reverse=True)[:top_k]
#         return [
#             {"document": doc, "metadata": meta, "score": float(score)}
#             for doc, meta, score in sorted_orig
#         ]
