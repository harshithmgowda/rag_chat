"""
Core Configuration
Loads environment variables and global application settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "PDF RAG Chatbot API"
    VERSION: str = "1.0.0"
    
    # NVIDIA NIM LLM Configuration (Meta LLaMA 3.1 70B)
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "meta/llama-3.1-70b-instruct")
    
    # LLM Hyperparameters
    TEMPERATURE: float = 0.2
    TOP_P: float = 0.7
    MAX_TOKENS: int = 1024

    # Embedding Settings (NVIDIA Nemotron-3-Embed-1B or local fallback)
    NVIDIA_EMBEDDING_API_KEY: str = os.getenv("NVIDIA_EMBEDDING_API_KEY", os.getenv("NVIDIA_API_KEY", ""))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "nvidia/nemotron-3-embed-1b")
    USE_NVIDIA_EMBEDDINGS: bool = os.getenv("USE_NVIDIA_EMBEDDINGS", "true").lower() == "true"

    # ChromaDB & Upload Storage
    CHROMA_DB_DIR: str = os.path.join("data", "chroma")
    COLLECTION_NAME: str = "pdf_rag_collection_nemotron"
    UPLOAD_DIR: str = "uploads"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
