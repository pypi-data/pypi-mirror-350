import os
import openai


class DeepSeekHelper:
    def __init__(self, base_url: str = None, api_key: str = None, model: str = None, embed_model: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.chat_model = model or os.getenv("DEEPSEEK_CHAT_MODEL", "deepseek-chat")
        self.embed_model = embed_model or os.getenv("DEEPSEEK_EMBED_MODEL", "deepseek-embedding")

        if not self.api_key:
            raise EnvironmentError("DEEPSEEK_API_KEY not set.")

        # Override OpenAI's API base and key
        openai.api_key = self.api_key
        openai.api_base = self.base_url

    def chat(self, messages: list, temperature: float = 0.7, max_tokens: int = 512):
        """
        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Explain quantum computing."}]
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Chat failed: {e}")

    def get_embedding(self, text: str):
        try:
            response = openai.Embedding.create(
                model=self.embed_model,
                input=[text]
            )
            return response['data'][0]['embedding']
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Embedding failed: {e}")

    def count_tokens(self, text: str):
        # Estimate: OpenAI-like token estimate
        return int(len(text.split()) * 1.33)

    def list_models(self):
        try:
            return openai.Model.list()
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Listing models failed: {e}")
