import os
import pytest
from unittest.mock import patch, MagicMock
from langxchange.openai_helper import OpenAIHelper


@pytest.fixture
def openai_helper(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    return OpenAIHelper()


@patch("openai.Embedding.create")
def test_get_embedding(mock_create, openai_helper):
    mock_create.return_value = {
        "data": [{"embedding": [0.1, 0.2, 0.3]}]
    }

    result = openai_helper.get_embedding("hello world")
    assert isinstance(result, list)
    assert result == [0.1, 0.2, 0.3]
    mock_create.assert_called_once()


@patch("openai.ChatCompletion.create")
def test_chat(mock_chat, openai_helper):
    mock_chat.return_value = {
        "choices": [{
            "message": {"content": "Quantum computing is a field..."}
        }]
    }

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is quantum computing?"}
    ]
    response = openai_helper.chat(messages)
    assert isinstance(response, str)
    assert "Quantum" in response or len(response) > 0


def test_count_tokens(openai_helper):
    text = "This is a test sentence with ten tokens more or less."
    tokens = openai_helper.count_tokens(text)
    assert isinstance(tokens, int)
    assert tokens > 0


@patch("openai.Model.list")
def test_list_models(mock_list, openai_helper):
    mock_list.return_value = {
        "data": [{"id": "gpt-3.5-turbo"}, {"id": "text-davinci-003"}]
    }

    result = openai_helper.list_models()
    assert isinstance(result, dict)
    assert "data" in result
