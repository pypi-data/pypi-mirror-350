import pytest
from unittest.mock import patch, MagicMock
from langxchange.google_genai_helper import GoogleGenAIHelper


@pytest.fixture
def google_genai_helper(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "")
    return GoogleGenAIHelper()


@patch("google.generativeai.GenerativeModel")
def test_generate_text(mock_model_cls, google_genai_helper):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Hello from Gemini!"
    mock_model_cls.return_value = mock_model

    prompt = "What is LangXchange?"
    result = google_genai_helper.generate_text(prompt)

    assert isinstance(result, str)
    assert "Hello" in result
    mock_model.generate_content.assert_called_once()


@patch("google.generativeai.get_model")
def test_get_embedding(mock_get_model, google_genai_helper):
    mock_model = MagicMock()
    mock_model.embed_content.return_value = {
        "embedding": [0.1, 0.2, 0.3]
    }
    mock_get_model.return_value = mock_model

    embedding = google_genai_helper.get_embedding("This is a test")
    assert isinstance(embedding, list)
    assert len(embedding) == 3


def test_count_tokens(google_genai_helper):
    prompt = "This is a token estimate test for GoogleGenAI."
    tokens = google_genai_helper.count_tokens(prompt)
    assert isinstance(tokens, int)
    assert tokens > 0


@patch("google.generativeai.list_models")
def test_list_models(mock_list_models, google_genai_helper):
    mock_list_models.return_value = ["models/chat-bison-001", "models/embedding-001"]

    models = google_genai_helper.list_models()
    assert isinstance(models, list)
    assert "models/embedding-001" in models
