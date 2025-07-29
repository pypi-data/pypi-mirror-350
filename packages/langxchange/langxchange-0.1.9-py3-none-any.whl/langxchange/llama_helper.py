# langxchange/llama_helper.py

import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer


class LLaMAHelper:
    """
    Helper class for interacting with LLaMA chat and embeddings via Hugging Face.
    """

    def __init__(
        self,
        chat_model: str = None,
        embed_model: str = None,
        hf_token: str = None,
        device: str = None
    ):
        """
        chat_model: HF model name for chat (e.g. "meta-llama/Llama-2-7b-chat-hf")
        embed_model: SentenceTransformer model name for embeddings
        hf_token: Hugging Face access token (or set HUGGINGFACE_TOKEN env var)
        device: "cpu" or "cuda" (auto-detected if None)
        """
        self.chat_model_name = chat_model or os.getenv(
            "LLAMA_CHAT_MODEL",
            "meta-llama/Llama-2-7b-chat-hf"
        )
        self.embed_model_name = embed_model or os.getenv(
            "LLAMA_EMBED_MODEL",
            "all-MiniLM-L6-v2"
        )

        # pick up token from param or env
        self.hf_token = hf_token or os.getenv("HUGGINGFACE_TOKEN")
        if not self.hf_token:
            raise EnvironmentError(
                "Hugging Face token required to access gated models. "
                "Set HUGGINGFACE_TOKEN env var or pass hf_token."
            )

        # Determine device
        self.device = device or ("cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu")

        # Load tokenizer and model with the access token
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.chat_model_name,
            use_auth_token=self.hf_token
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.chat_model_name,
            use_auth_token=self.hf_token,
            device_map="auto" if self.device.startswith("cuda") else None
        )
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device.startswith("cuda") else -1,
            use_auth_token=self.hf_token
        )

        # Embedding model (public)
        self.embedder = SentenceTransformer(
            self.embed_model_name,
            device=self.device
        )

    def generate_text(
        self,
        prompt: str,
        max_length: int = 256,
        temperature: float = 0.7,
        do_sample: bool = True,
    ) -> str:
        try:
            results = self.generator(
                prompt,
                max_length=max_length,
                do_sample=do_sample,
                temperature=temperature,
                return_full_text=False
            )
            return results[0]["generated_text"]
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to generate text: {e}")

    def chat(
        self,
        messages: list,
        max_length: int = 256,
        temperature: float = 0.7,
        do_sample: bool = True,
    ) -> str:
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            tag = role.upper()
            prompt_parts.append(f"[{tag}]\n{content}\n")
        prompt = "\n".join(prompt_parts) + "[ASSISTANT]\n"

        return self.generate_text(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature,
            do_sample=do_sample
        )

    def get_embedding(self, text: str) -> list:
        try:
            emb = self.embedder.encode(text)
            return emb.tolist() if hasattr(emb, "tolist") else list(emb)
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to generate embedding: {e}")

    def count_tokens(self, prompt: str) -> int:
        return len(self.tokenizer.tokenize(prompt))
