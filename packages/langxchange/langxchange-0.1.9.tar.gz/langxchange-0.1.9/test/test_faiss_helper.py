import pytest
import numpy as np
from langxchange.faiss_helper import FAISSHelper


@pytest.fixture
def faiss_helper():
    return FAISSHelper(dim=4)  # small dim for test simplicity


def test_insert_and_count(faiss_helper):
    vectors = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.2, 0.1, 0.6]]
    documents = ["Hello world", "LangXchange is awesome"]
    metadatas = [{"source": "unit"}, {"source": "test"}]

    ids = faiss_helper.insert(vectors, documents, metadatas)
    assert len(ids) == 2
    assert faiss_helper.count() == 2


def test_query_results(faiss_helper):
    vectors = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.2, 0.1, 0.6]]
    documents = ["Document A", "Document B"]
    faiss_helper.insert(vectors, documents)

    query_vector = [0.1, 0.2, 0.3, 0.4]
    results = faiss_helper.query(query_vector, top_k=2)

    assert isinstance(results, list)
    assert len(results) <= 2
    assert "text" in results[0]
    assert "metadata" in results[0]


def test_query_no_results(faiss_helper):
    query_vector = [0.0, 0.0, 0.0, 0.0]
    results = faiss_helper.query(query_vector, top_k=3)

    assert isinstance(results, list)
    # No documents inserted yet, so should be empty or safe fallback
    assert len(results) == 0 or all("text" in r for r in results)
