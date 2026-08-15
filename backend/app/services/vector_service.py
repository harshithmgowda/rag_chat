"""
Vector Database Service (ChromaDB)
Manages saving, indexing, and querying document vectors with metadata.
"""
import os
import chromadb

class VectorService:
    def __init__(self, db_path: str = os.path.join("data", "chroma"), collection_name: str = "pdf_rag_collection"):
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "RAG Document Knowledge Base"}
        )

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]):
        """
        Stores chunk text, embeddings, and metadata into ChromaDB.
        """
        if not chunks:
            return 0

        ids = [c["chunk_id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [
            {
                "page_number": c["page_number"],
                "doc_name": c["doc_name"],
                "char_count": c.get("char_count", len(c["text"]))
            }
            for c in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        return len(chunks)

    def search_similar(self, query_vector: list[float], top_k: int = 3, doc_name: str = None) -> list[dict]:
        """
        Performs semantic similarity search with optional filtering by doc_name.
        """
        where_filter = {"doc_name": doc_name} if doc_name else None

        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )

        matched_items = []
        if not results or not results["ids"] or len(results["ids"][0]) == 0:
            return matched_items

        for idx in range(len(results["ids"][0])):
            matched_items.append({
                "chunk_id": results["ids"][0][idx],
                "text": results["documents"][0][idx],
                "page_number": results["metadatas"][0][idx].get("page_number", 1),
                "doc_name": results["metadatas"][0][idx].get("doc_name", "unknown.pdf"),
                "distance": results["distances"][0][idx]
            })

        return matched_items

    def count(self) -> int:
        return self.collection.count()
