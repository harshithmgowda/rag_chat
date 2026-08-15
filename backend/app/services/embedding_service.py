"""
Embedding Service
Provides text embedding vectors using sentence-transformers model (all-MiniLM-L6-v2).
"""
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls, model_name: str = "all-MiniLM-L6-v2"):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._model = SentenceTransformer(model_name)
        return cls._instance

    def embed_text(self, text: str) -> list[float]:
        """Embeds a single query string into a vector."""
        return self._model.encode(text).tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embeds a list of chunk texts in batch."""
        return self._model.encode(texts).tolist()
