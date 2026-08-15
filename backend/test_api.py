"""
API Test Suite (using FastAPI TestClient)
Verifies:
1. GET /api/health
2. POST /api/upload (Uploads sample_document.pdf)
3. GET /api/documents
4. POST /api/chat (Asks questions to the uploaded document)
"""
import os
import sys
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app

client = TestClient(app)

def test_health_check():
    print("=" * 60)
    print("1. TESTING GET /api/health")
    response = client.get("/api/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health Check Passed!\n")

def test_upload_pdf():
    print("=" * 60)
    print("2. TESTING POST /api/upload")
    pdf_path = "sample_document.pdf"
    
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": (pdf_path, f, "application/pdf")}
        )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 201
    assert response.json()["total_pages"] == 3
    print("✅ PDF Upload & Ingestion API Passed!\n")

def test_list_documents():
    print("=" * 60)
    print("3. TESTING GET /api/documents")
    response = client.get("/api/documents")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert "sample_document.pdf" in response.json()["documents"]
    print("✅ Document Listing API Passed!\n")

def test_chat():
    print("=" * 60)
    print("4. TESTING POST /api/chat")
    payload = {
        "question": "What is the policy regarding API keys and credential leaks?",
        "doc_name": "sample_document.pdf",
        "top_k": 2
    }
    response = client.post("/api/chat", json=payload)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"🤖 Bot Answer:\n{data['answer']}")
    print(f"📚 Sources: {data['sources']}")
    assert response.status_code == 200
    assert len(data["sources"]) > 0
    print("✅ RAG Chat API Passed!\n")

if __name__ == "__main__":
    test_health_check()
    test_upload_pdf()
    test_list_documents()
    test_chat()
    print("=" * 60)
    print("🎉 ALL FASTAPI ENDPOINTS VERIFIED AND WORKING!")
    print("=" * 60)
