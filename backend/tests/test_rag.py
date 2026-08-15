"""
Comprehensive Test Suite for RAG Pipeline (Unit & Integration Tests)
Run with: pytest backend/tests/test_rag.py -v
"""
import os
import sys
import pytest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.services.chunking_service import split_text_into_chunks, chunk_extracted_pages
from backend.app.services.pdf_service import extract_text_from_pdf
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_service import VectorService
from backend.app.services.rag_service import RAGService
from backend.embeddings_demo import cosine_similarity_manual

class TestChunking:
    def test_split_text_basic(self):
        text = "Hello world this is a test of chunking."
        chunks = split_text_into_chunks(text, chunk_size=20, chunk_overlap=5)
        assert len(chunks) > 0
        assert all(len(c) <= 20 for c in chunks)

    def test_invalid_overlap_raises_error(self):
        with pytest.raises(ValueError):
            split_text_into_chunks("Test", chunk_size=50, chunk_overlap=50)

    def test_chunk_extracted_pages_preserves_page_numbers(self):
        mock_pages = [
            {"page_number": 1, "text": "Page one content.", "doc_name": "test.pdf"},
            {"page_number": 2, "text": "Page two content.", "doc_name": "test.pdf"}
        ]
        chunks = chunk_extracted_pages(mock_pages, chunk_size=50, chunk_overlap=10)
        assert len(chunks) == 2
        assert chunks[0]["page_number"] == 1
        assert chunks[1]["page_number"] == 2


class TestEmbeddings:
    def test_cosine_similarity_identical(self):
        vec_a = [1.0, 2.0, 3.0]
        vec_b = [1.0, 2.0, 3.0]
        sim = cosine_similarity_manual(vec_a, vec_b)
        assert pytest.approx(sim, 0.001) == 1.0

    def test_cosine_similarity_orthogonal(self):
        vec_a = [1.0, 0.0]
        vec_b = [0.0, 1.0]
        sim = cosine_similarity_manual(vec_a, vec_b)
        assert pytest.approx(sim, 0.001) == 0.0

    def test_embedding_dimensions(self):
        service = EmbeddingService()
        vec = service.embed_text("Testing embeddings")
        # NVIDIA Nemotron is 2048 dims, MiniLM is 384 dims
        assert len(vec) in [384, 1024, 2048]


class TestVectorStoreAndMultiplePDFs:
    def test_metadata_filtering_by_doc_name(self):
        vec_service = VectorService(collection_name="test_multi_doc_nemotron_col")
        # Clean collection for test
        try:
            vec_service.client.delete_collection(name="test_multi_doc_nemotron_col")
            vec_service = VectorService(collection_name="test_multi_doc_nemotron_col")
        except Exception:
            pass

        chunks_a = [{
            "chunk_id": "doc_a_1",
            "text": "Apples are delicious red fruits.",
            "page_number": 1,
            "doc_name": "doc_a.pdf"
        }]
        chunks_b = [{
            "chunk_id": "doc_b_1",
            "text": "Quantum computers use qubits for computation.",
            "page_number": 1,
            "doc_name": "doc_b.pdf"
        }]
        
        emb_service = EmbeddingService()
        vec_a = emb_service.embed_documents(["Apples are delicious red fruits."])
        vec_b = emb_service.embed_documents(["Quantum computers use qubits for computation."])
        
        vec_service.add_chunks(chunks_a, vec_a)
        vec_service.add_chunks(chunks_b, vec_b)
        
        query_vec = emb_service.embed_text("fruits and apples")
        
        results = vec_service.search_similar(query_vec, top_k=2, doc_name="doc_b.pdf")
        if results:
            assert all(r["doc_name"] == "doc_b.pdf" for r in results)
