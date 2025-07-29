# langxchange/google_genai_helper.py

import os
from google import genai
from google.genai import types


class GoogleGenAIHelper:
    """
    Helper class for interacting with Google Gemini via the `google-genai` client.
    """

    def __init__(
        self,
        api_key: str = None,
        chat_model: str = None,
        embed_model: str = None,
    ):
        """
        api_key: Your Google API key (or use GOOGLE_API_KEY env var)
        chat_model: The Gemini chat model name (e.g., "gemini-2.0-flash")
        embed_model: The embedding model name (e.g., "models/embedding-gecko-001")
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GOOGLE_API_KEY not set in environment.")

        # Initialize the client
        self.client = genai.Client(api_key=self.api_key)
        
        # print( self.client)
        self.chat_model = chat_model or os.getenv("GOOGLE_CHAT_MODEL", "gemini-2.0-flash")
        self.embed_model = embed_model or os.getenv("GOOGLE_EMBED_MODEL", "models/text-embedding-004")

    def chat(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        Perform a chat-style completion using Gemini.

        messages: list of dicts, e.g.:
          [
            {"role": "system",  "content": "You are a helpful assistant."},
            {"role": "user",    "content": "Explain quantum computing."}
          ]

        max_tokens: maximum tokens to generate.

        Returns the assistant's reply text.
        """
        # Build a list of plain strings to pass as 'contents'
        # Each message becomes "[ROLE]\n<content>"
        contents = [
            f"[{msg['role'].upper()}]\n{msg['content'].strip()}"
            for msg in messages
        ]

        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        response = self.client.models.generate_content(
            model=self.chat_model,
            contents=contents,
            config=config,
        )
        print(response.text)
        return response.text

    def get_embedding(self, text: str) -> list:
        """
        Generate an embedding vector for the given text.
        """
        title = "Custom query"
        result = self.client.models.embed_content(
            model=self.embed_model,
            contents=text,
            # config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
            config=types.EmbedContentConfig(
                task_type="retrieval_document",
                title=title
                        )
            )
        # request = types.EmbedTextRequest(
        #     model=self.embed_model,
        #     text=[text],
        # )
        # resp = self.client.embeddings.embed_text(request=request)
        return result.embeddings[0].values

    # def get_embedding(self, text: str) -> list:
    #     """
    #     Generate an embedding vector for the given text.
    #     Raises RuntimeError if the API returns no embedding.
    #     """
    #     request = types.EmbedTextRequest(
    #         model=self.embed_model,
    #         text=[text],
    #     )
    #     resp = self.client.embeddings.embed_text(request=request)

    #     # resp.embeddings should be a list of lists
    #     if not hasattr(resp, "embeddings") or not resp.embeddings:
    #         raise RuntimeError(f"[❌ ERROR] Empty embeddings response: {resp!r}")

    #     embedding = resp.embeddings[0]
    #     if embedding is None or not isinstance(embedding, (list, tuple)):
    #         raise RuntimeError(f"[❌ ERROR] Invalid embedding returned: {embedding!r}")

    #     return embedding
    

    def count_tokens(self, prompt: str) -> int:
        """
        Rough token count: approximate 1 token ≈ 0.75 words.
        """
        return int(len(prompt.split()) / 0.75)

    def list_chat_models(self) -> list:
        """
        List available chat models.
        """
        return [m.name for m in self.client.models.list()]

    def list_embed_models(self) -> list:
        """
        List available embedding models.
        """
        return [m.name for m in self.client.embeddings.list()]
