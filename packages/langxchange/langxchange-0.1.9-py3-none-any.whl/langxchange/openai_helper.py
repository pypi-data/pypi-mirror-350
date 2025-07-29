import os
import openai

class OpenAIHelper:
    
    def __init__(self, model: str = None, embedding_model: str = None):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY not set in environment.")

        openai.api_key = self.api_key

        self.chat_model = model or os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
        self.embedding_model = embedding_model or os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")

    def get_embedding(self, text: str) -> list:
        try:
            response = openai.Embedding.create(
                input=[text],
                model=self.embedding_model
            )
            return response['data'][0]['embedding']
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to get embedding: {e}")

    def chat(self, messages: list, temperature: float = 0.7, max_tokens: int = 512):
        """
        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Explain quantum computing."}]
        """

        print(messages)
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Chat completion failed: {e}")

    def count_tokens(self, prompt: str, model: str = None):
        """Estimate tokens for simple strings (approximate)."""
        model = model or self.chat_model
        if "gpt-3.5" in model or "gpt-4" in model:
            return int(len(prompt.split()) * 1.5)  # very rough estimate
        return len(prompt.split())

    def list_models(self):
        try:
            return openai.Model.list()
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Could not list OpenAI models: {e}")
