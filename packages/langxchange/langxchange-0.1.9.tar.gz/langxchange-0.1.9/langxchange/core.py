import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from .utils import load_data

class LangXchangeAPI:
    def __init__(self, llm_provider="openai", model_name="text-embedding-ada-002"):
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def ingest(self, source, source_type="csv", text_column="text"):
        self.data = load_data(source, source_type)
        self.texts = self.data[text_column].tolist()
        return self.texts

    def vectorize(self):
        if not hasattr(self, "texts"):
            raise ValueError("No data loaded. Use `.ingest()` first.")
        self.vectors = self.embedding_model.encode(self.texts, show_progress_bar=True)
        return self.vectors

    def get_vector(self, text):
        return self.embedding_model.encode([text])[0]
