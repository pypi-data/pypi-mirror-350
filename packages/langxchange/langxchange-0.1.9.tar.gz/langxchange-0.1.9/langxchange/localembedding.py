import os
import time
from sentence_transformers import SentenceTransformer

class LocalEmbedder:
    """
    Simple wrapper to expose a .embed(texts) method over SentenceTransformer.
    """
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        arrs = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return [vec.tolist() for vec in arrs]