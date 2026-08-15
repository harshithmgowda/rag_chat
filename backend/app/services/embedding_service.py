"""
Embedding Service
Provides 2048-dimensional dense vector embeddings using NVIDIA Nemotron-3-Embed-1B (or local SentenceTransformers fallback).
"""
import os
from openai import OpenAI
from backend.app.core.config import settings

class EmbeddingService:
    _instance = None
    _client = None
    _local_model = None

    def __new__(cls, model_name: str = None):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._model_name = model_name or settings.EMBEDDING_MODEL
            cls._use_nvidia = settings.USE_NVIDIA_EMBEDDINGS and bool(settings.NVIDIA_EMBEDDING_API_KEY)

            if cls._use_nvidia:
                print(f"🚀 Initializing Cloud Embeddings with NVIDIA NIM: {cls._model_name}")
                cls._client = OpenAI(
                    base_url=settings.NVIDIA_BASE_URL,
                    api_key=settings.NVIDIA_EMBEDDING_API_KEY
                )
            else:
                print(f"💻 Initializing Local Embeddings (SentenceTransformers): all-MiniLM-L6-v2")
                from sentence_transformers import SentenceTransformer
                cls._local_model = SentenceTransformer('all-MiniLM-L6-v2')

        return cls._instance

    def embed_text(self, text: str) -> list[float]:
        """Embeds a single query string into a vector."""
        if self._use_nvidia:
            response = self._client.embeddings.create(
                input=[text],
                model=self._model_name
            )
            return response.data[0].embedding
        else:
            return self._local_model.encode(text).tolist()

    def embed_documents(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """Embeds a list of chunk texts in batches."""
        if not texts:
            return []

        if self._use_nvidia:
            all_embeddings = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self._client.embeddings.create(
                    input=batch,
                    model=self._model_name
                )
                all_embeddings.extend([item.embedding for item in response.data])
            return all_embeddings
        else:
            return self._local_model.encode(texts).tolist()
