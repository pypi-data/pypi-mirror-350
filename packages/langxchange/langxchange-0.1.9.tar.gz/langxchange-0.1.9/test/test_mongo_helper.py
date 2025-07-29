import os
import pytest
import pandas as pd
import mongomock
from unittest.mock import patch
from langxchange.mongo_helper import MongoHelper


@pytest.fixture
def mock_mongo_env(monkeypatch):
    monkeypatch.setenv("MONGO_URI", "mongodb://127.0.0.1:27017")
    monkeypatch.setenv("MONGO_DB", "test_db")
    monkeypatch.setenv("MONGO_COLLECTION", "test_collection")


@patch("pymongo.MongoClient", new_callable=mongomock.MongoClient)
def test_insert_dataframe_and_query(mock_client, mock_mongo_env):
    helper = MongoHelper(db_name="test_db", collection_name="test_collection")
    helper.client = mock_client
    helper.db = mock_client["test_db"]
    helper.collection = helper.db["test_collection"]

    # Insert a DataFrame
    df = pd.DataFrame([
        {"name": "Alice", "age": 28},
        {"name": "Bob", "age": 34}
    ])
    inserted_ids = helper.insert(df)
    assert len(inserted_ids) == 2

    # Query all data
    result_df = helper.query()
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape[0] == 2
    assert "name" in result_df.columns


@patch("pymongo.MongoClient", new_callable=mongomock.MongoClient)
def test_insert_list_and_count(mock_client, mock_mongo_env):
    helper = MongoHelper(db_name="test_db", collection_name="test_collection")
    helper.client = mock_client
    helper.db = mock_client["test_db"]
    helper.collection = helper.db["test_collection"]

    # Insert a list of dicts
    docs = [{"title": "LangXchange Test"}, {"title": "Vector DBs"}]
    inserted = helper.insert(docs)
    assert len(inserted) == 2

    # Check count
    assert helper.count() == 2


@patch("pymongo.MongoClient", new_callable=mongomock.MongoClient)
def test_query_with_filter(mock_client, mock_mongo_env):
    helper = MongoHelper(db_name="test_db", collection_name="test_collection")
    helper.client = mock_client
    helper.db = mock_client["test_db"]
    helper.collection = helper.db["test_collection"]

    # Insert documents
    helper.insert([
        {"category": "AI"},
        {"category": "Dev"},
        {"category": "AI"}
    ])

    # Query filtered
    result = helper.query(filter_query={"category": "AI"})
    assert result.shape[0] == 2
