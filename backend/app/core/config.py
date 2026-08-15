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
    
    # NVIDIA NIM / OpenAI settings
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "meta/llama-3.1-70b-instruct")
    
    # LLM Hyperparameters
    TEMPERATURE: float = 0.2
    TOP_P: float = 0.7
    MAX_TOKENS: int = 1024

    # Embedding & Vector DB settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHROMA_DB_DIR: str = os.path.join("data", "chroma")
    COLLECTION_NAME: str = "pdf_rag_collection"

    # Uploads Directory
    UPLOAD_DIR: str = "uploads"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
