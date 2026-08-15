"""
FastAPI Main Application Entry Point
Exposes REST API endpoints for PDF Upload, RAG Question Answering, and Health Checks.
"""
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure root path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from backend.app.core.config import settings
from backend.app.api.routes.upload import router as upload_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.services.vector_service import VectorService
from backend.app.schemas.chat import HealthResponse

# 1. Initialize FastAPI Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-ready RAG backend for querying uploaded PDF documents with Meta LLaMA 3.1 & ChromaDB."
)

# 2. Add CORS Middleware (Permits React frontend on any port to communicate seamlessly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include API Routes
app.include_router(upload_router)
app.include_router(chat_router)

# 4. Health Check Endpoint
@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Returns server status, version, and the number of indexed chunks in ChromaDB.
    """
    vec_service = VectorService(
        db_path=settings.CHROMA_DB_DIR,
        collection_name=settings.COLLECTION_NAME
    )
    return HealthResponse(
        status="healthy",
        project=settings.PROJECT_NAME,
        version=settings.VERSION,
        total_chunks_indexed=vec_service.count()
    )

@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Welcome to PDF RAG Chatbot API!",
        "interactive_docs": "/docs",
        "health_check": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
