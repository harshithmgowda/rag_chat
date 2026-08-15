"""
Chat API Route
Handles questions from the frontend, queries the vector database, and returns LLM answers.
"""
import os
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.chat import ChatRequest, ChatResponse, RetrievedChunkInfo
from backend.app.services.rag_service import RAGService
from backend.app.core.config import settings

router = APIRouter(prefix="/api", tags=["RAG Chat"])
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_pdf(request: ChatRequest):
    """
    Receives a question from the user and optional document filter, performs semantic search,
    and returns a factual grounded answer with page sources.
    """
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty!"
        )

    try:
        result = rag_service.ask(
            question=request.question,
            doc_name=request.doc_name,
            top_k=request.top_k
        )

        formatted_chunks = [
            RetrievedChunkInfo(
                chunk_id=c["chunk_id"],
                doc_name=c["doc_name"],
                page_number=c["page_number"],
                text=c["text"],
                distance=round(c["distance"], 4)
            )
            for c in result.get("retrieved_chunks", [])
        ]

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            retrieved_chunks=formatted_chunks
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating answer: {str(e)}"
        )


@router.get("/documents", tags=["Documents"])
async def list_uploaded_documents():
    """
    Lists all uploaded PDF documents currently available on the server.
    """
    if not os.path.exists(settings.UPLOAD_DIR):
        return {"documents": []}

    files = [f for f in os.listdir(settings.UPLOAD_DIR) if f.lower().endswith(".pdf")]
    return {
        "count": len(files),
        "documents": files
    }
