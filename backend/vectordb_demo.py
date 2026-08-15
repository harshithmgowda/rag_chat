"""
Phase 5: Vector Database (ChromaDB)
Demonstrates storing chunks, embeddings, and metadata in a persistent ChromaDB database
and performing high-speed semantic search.
"""
import sys
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pymupdf

# Ensure Windows terminal outputs UTF-8 characters cleanly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def split_text_into_chunks(text: str, chunk_size: int = 250, chunk_overlap: int = 40):
    chunks = []
    start = 0
    step = chunk_size - chunk_overlap
    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def build_and_query_vectordb():
    print("=" * 70)
    print("🗄️ INITIALIZING CHROMADB VECTOR DATABASE")
    print("=" * 70)

    # 1. Initialize persistent storage in the 'data/chroma' directory
    db_path = os.path.join("data", "chroma")
    os.makedirs(db_path, exist_ok=True)
    
    client = chromadb.PersistentClient(path=db_path)
    
    # 2. Create or get a Collection (like creating a table in SQL)
    collection_name = "pdf_knowledge_base"
    
    # Reset collection for clean demo run
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "PDF Document Chunks & Embeddings"}
    )
    print(f"✅ Collection '{collection_name}' created in: {os.path.abspath(db_path)}")

    # 3. Load Embedding Model
    print("\n🧠 Loading Embedding Model (all-MiniLM-L6-v2)...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    # 4. Extract & Chunk PDF
    pdf_path = "sample_document.pdf"
    print(f"\n📄 Ingesting document: {pdf_path}")
    doc = pymupdf.open(pdf_path)

    documents = []  # The chunk text
    embeddings = [] # The vector coordinates
    metadatas = []  # Extra details (page number, source filename)
    ids = []        # Unique IDs

    global_id = 0
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1
        raw_text = page.get_text("text").strip()
        page_chunks = split_text_into_chunks(raw_text, chunk_size=250, chunk_overlap=40)

        for chunk_idx, chunk_text in enumerate(page_chunks):
            global_id += 1
            chunk_id = f"doc1_p{page_num}_c{chunk_idx + 1}"
            
            # Generate embedding vector for this chunk
            vector = embedding_model.encode(chunk_text).tolist()

            ids.append(chunk_id)
            documents.append(chunk_text)
            embeddings.append(vector)
            metadatas.append({
                "page_number": page_num,
                "doc_name": os.path.basename(pdf_path),
                "char_length": len(chunk_text)
            })

    doc.close()

    # 5. Store everything in ChromaDB
    print(f"📦 Storing {len(documents)} chunks with embeddings into ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"✅ Stored {collection.count()} items in ChromaDB successfully!")

    # 6. Perform Vector Similarity Search
    print("\n" + "=" * 70)
    print("🔍 TESTING SEMANTIC SEARCH IN CHROMADB")
    print("=" * 70)

    test_queries = [
        "What are the different process states in an operating system?",
        "What is the policy for API keys and secrets?",
        "Why do LLMs hallucinate and how does RAG help?"
    ]

    for q_idx, query in enumerate(test_queries, 1):
        print(f"\n❓ Query {q_idx}: \"{query}\"")
        
        # Convert user query into an embedding vector
        query_vec = embedding_model.encode(query).tolist()

        # Query ChromaDB for top 2 closest matching chunks
        results = collection.query(
            query_embeddings=[query_vec],
            n_results=2,
            include=["documents", "metadatas", "distances"]
        )

        print("   🎯 Top Matching Results:")
        for rank in range(len(results["ids"][0])):
            res_id = results["ids"][0][rank]
            res_meta = results["metadatas"][0][rank]
            res_doc = results["documents"][0][rank]
            res_dist = results["distances"][0][rank] # Smaller distance = closer match!

            print(f"   [{rank + 1}] ID: {res_id} | 📄 Source: Page {res_meta['page_number']} (Distance: {res_dist:.4f})")
            print(f"       Snippet: \"{res_doc[:90]}...\"\n")

    print("=" * 70)
    print("🎉 ChromaDB Vector Database is working perfectly!")
    print("=" * 70)

if __name__ == "__main__":
    build_and_query_vectordb()
