import pytest
import uuid
import numpy as np
from unittest.mock import patch, MagicMock
from langxchange.opensearch_helper import OpenSearchHelper


@pytest.fixture
def sample_data():
    vectors = np.random.rand(2, 384).tolist()
    documents = ["First document", "Second document"]
    metadatas = [{"author": "Alice"}, {"author": "Bob"}]
    return vectors, documents, metadatas


@patch("langxchange.opensearch_helper.OpenSearch")
@patch("langxchange.opensearch_helper.helpers.bulk")
def test_insert(mock_bulk, mock_client, sample_data):
    mock_client.return_value.indices.exists.return_value = False
    mock_client.return_value.indices.create.return_value = {"acknowledged": True}

    helper = OpenSearchHelper(index_name="test_index", dim=384)
    helper.client = mock_client.return_value  # inject mock client

    vectors, docs, metas = sample_data
    inserted_ids = helper.insert(vectors, docs, metas)
    assert len(inserted_ids) == 2
    mock_bulk.assert_called_once()


@patch("langxchange.opensearch_helper.OpenSearch")
def test_query(mock_client):
    mock_response = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "text": "Test result",
                        "metadata": {"type": "test"}
                    },
                    "_score": 0.99
                }
            ]
        }
    }

    mock_client.return_value.search.return_value = mock_response
    mock_client.return_value.indices.exists.return_value = True

    helper = OpenSearchHelper(index_name="test_index", dim=384)
    helper.client = mock_client.return_value

    result = helper.query([0.1] * 384, top_k=1)
    assert len(result) == 1
    assert result[0]["text"] == "Test result"
    assert result[0]["score"] == 0.99
