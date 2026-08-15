"""
Pydantic Schemas for API Request & Response Validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The user's question to ask the PDF")
    doc_name: Optional[str] = Field(None, description="Optional: specific PDF document name to restrict search to")
    top_k: int = Field(3, ge=1, le=10, description="Number of context chunks to retrieve")

class RetrievedChunkInfo(BaseModel):
    chunk_id: str
    doc_name: str
    page_number: int
    text: str
    distance: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    retrieved_chunks: List[RetrievedChunkInfo] = []

class UploadResponse(BaseModel):
    filename: str
    total_pages: int
    total_chunks: int
    message: str

class HealthResponse(BaseModel):
    status: str
    project: str
    version: str
    total_chunks_indexed: int
