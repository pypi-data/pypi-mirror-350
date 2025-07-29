import pytest
from unittest.mock import patch, MagicMock
from langxchange.llama_helper import LLaMAHelper


@patch("langxchange.llama_helper.SentenceTransformer")
@patch("langxchange.llama_helper.pipeline")
@patch("langxchange.llama_helper.AutoModelForCausalLM.from_pretrained")
@patch("langxchange.llama_helper.AutoTokenizer.from_pretrained")
def test_generate_and_embed(
    mock_tokenizer, mock_model, mock_pipeline, mock_embedder
):
    # Mock tokenizer and model
    mock_tokenizer.return_value = MagicMock()
    mock_model.return_value = MagicMock()
    
    # Mock pipeline
    mock_gen = MagicMock()
    mock_gen.return_value = [{"generated_text": "Hello from LLaMA"}]
    mock_pipeline.return_value = mock_gen

    # Mock embedder
    mock_embed = MagicMock()
    mock_embed.encode.return_value = [0.1, 0.2, 0.3]
    mock_embedder.return_value = mock_embed

    # Instantiate helper
    llama = LLaMAHelper(chat_model="fake-model", embed_model="fake-embed")

    # Run generate_text
    result = llama.generate_text("What is LangXchange?")
    assert isinstance(result, str)
    assert "Hello" in result

    # Run get_embedding
    embedding = llama.get_embedding("Test embedding")
    assert isinstance(embedding, list)
    assert len(embedding) == 3
