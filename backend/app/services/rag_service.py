"""
RAG Pipeline Service
Orchestrates PDF Ingestion, Semantic Retrieval, Prompt Assembly, and LLM Generation
using NVIDIA NIM (meta/llama-3.1-70b-instruct).
"""
import os
from openai import OpenAI

from backend.app.core.config import settings
from backend.app.services.pdf_service import extract_text_from_pdf
from backend.app.services.chunking_service import chunk_extracted_pages
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_service import VectorService

class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService(model_name=settings.EMBEDDING_MODEL)
        self.vector_service = VectorService(
            db_path=settings.CHROMA_DB_DIR,
            collection_name=settings.COLLECTION_NAME
        )
        
        # Initialize OpenAI/NVIDIA API client
        self.llm_client = OpenAI(
            base_url=settings.NVIDIA_BASE_URL,
            api_key=settings.NVIDIA_API_KEY
        )

    def ingest_pdf(self, pdf_path: str, chunk_size: int = 350, chunk_overlap: int = 50) -> dict:
        """
        Ingests ANY uploaded PDF file:
        1. Extracts text and page numbers
        2. Splits into overlapping chunks
        3. Generates embedding vectors
        4. Upserts into ChromaDB
        """
        # Step 1: Extract Text
        pages = extract_text_from_pdf(pdf_path)
        if not pages:
            raise ValueError("No extractable text found in this PDF! Make sure it has a digital text layer.")

        # Step 2: Chunk Text
        chunks = chunk_extracted_pages(pages, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        # Step 3: Embed Chunks
        chunk_texts = [c["text"] for c in chunks]
        embeddings = self.embedding_service.embed_documents(chunk_texts)

        # Step 4: Save to ChromaDB
        stored_count = self.vector_service.add_chunks(chunks, embeddings)

        return {
            "doc_name": os.path.basename(pdf_path),
            "pages_count": len(pages),
            "chunks_count": stored_count
        }

    def ask(self, question: str, doc_name: str = None, top_k: int = 3) -> dict:
        """
        Retrieves context and asks Meta LLaMA-3.1-70B on NVIDIA NIM:
        """
        # Step 1: Embed Question
        query_vector = self.embedding_service.embed_text(question)

        # Step 2: Retrieve Top-K chunks
        retrieved_chunks = self.vector_service.search_similar(query_vector, top_k=top_k, doc_name=doc_name)

        if not retrieved_chunks:
            return {
                "answer": "I couldn't find any relevant information in the uploaded document.",
                "sources": [],
                "retrieved_chunks": []
            }

        # Step 3: Format Context and Sources
        context_parts = []
        sources = []
        for c in retrieved_chunks:
            context_parts.append(f"[Document: {c['doc_name']}, Page: {c['page_number']}]\n{c['text']}")
            source_tag = f"Page {c['page_number']} ({c['doc_name']})"
            if source_tag not in sources:
                sources.append(source_tag)

        context_text = "\n\n".join(context_parts)

        # Step 4: Create Grounded System Prompt
        system_prompt = (
            "You are an expert AI assistant that answers user questions based STRICTLY and ONLY on the provided PDF context.\n"
            "Rules:\n"
            "1. Answer using ONLY the facts from the context below.\n"
            "2. If the context does not contain enough information to answer the question, say: "
            "'I couldn't find this information in the uploaded document.'\n"
            "3. Do NOT invent facts or use external knowledge.\n"
            "4. Always mention the page number(s) where the facts were found."
        )

        user_prompt = f"--- CONTEXT FROM UPLOADED PDF ---\n{context_text}\n--- END OF CONTEXT ---\n\nUSER QUESTION: {question}"

        # Step 5: Call LLM with user's specific hyperparameters
        response = self.llm_client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=settings.TEMPERATURE,
            top_p=settings.TOP_P,
            max_tokens=settings.MAX_TOKENS,
            stream=False
        )

        answer = response.choices[0].message.content.strip() if response.choices[0].message.content else ""

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": retrieved_chunks
        }
