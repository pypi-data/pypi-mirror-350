import os
import uuid
import pandas as pd
import pytest
from langxchange.chroma_helper import ChromaHelper

@pytest.fixture(scope="module")
def chroma_helper(tmp_path_factory):
    os.environ["CHROMA_PERSIST_PATH"] = str(tmp_path_factory.mktemp("chroma_test_store"))
    os.environ["OPENAI_API_KEY"] = "sk-test"  # mocked or fake key for test
    return ChromaHelper()

def test_insert_and_count(chroma_helper):
    docs = ["Hello world", "LangXchange rocks"]
    embeddings = [[0.1] * 1536, [0.2] * 1536]
    metadatas = [{"source": "unit_test"}, {"source": "unit_test"}]  # ✅ Not empty
    ids = chroma_helper.insert("test_collection", documents=docs, embeddings=embeddings, metadatas=metadatas)
    assert len(ids) == 2
    count = chroma_helper.get_collection_count("test_collection")
    assert count == 2

def test_ingest_to_chroma(chroma_helper):
    df = pd.DataFrame({
        "documents": ["AI is the future", "Build with LangXchange"],
        "source": ["test1", "test2"]
    })
    count = chroma_helper.ingest_to_chroma(df, collection_name="batch_test", engine="openai")
    assert count == 2

def test_query(chroma_helper):
    embedding = [0.1] * 1536
    result = chroma_helper.query("test_collection", embedding_vector=embedding)
    assert "documents" in result