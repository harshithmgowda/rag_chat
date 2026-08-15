"""
Upload API Route
Handles file uploading, validation, and triggering the RAG ingestion pipeline.
"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from backend.app.schemas.chat import UploadResponse
from backend.app.services.rag_service import RAGService
from backend.app.core.config import settings

router = APIRouter(prefix="/api", tags=["PDF Ingestion"])
rag_service = RAGService()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Receives ANY PDF uploaded from the web browser, saves it, and processes it into ChromaDB.
    """
    # 1. Validate File Extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type! Only PDF documents (.pdf) are supported."
        )

    # 2. Secure file destination path
    safe_filename = os.path.basename(file.filename)
    dest_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    # 3. Save uploaded file to disk
    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file on server: {str(e)}"
        )
    finally:
        file.file.close()

    # 4. Ingest and index PDF in RAG pipeline
    try:
        stats = rag_service.ingest_pdf(dest_path)
        return UploadResponse(
            filename=stats["doc_name"],
            total_pages=stats["pages_count"],
            total_chunks=stats["chunks_count"],
            message=f"Successfully processed and indexed {stats['pages_count']} pages into vector database!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to extract and index PDF: {str(e)}"
        )
