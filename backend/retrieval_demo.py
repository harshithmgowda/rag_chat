"""
Phase 6: Retrieval Engine & Top-K Tradeoffs
Demonstrates how to build a dedicated Retriever module that takes any user question,
converts it into a vector, and queries ChromaDB for the Top-K most relevant chunks.
"""
import sys
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Ensure Windows terminal outputs UTF-8 characters cleanly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

class DocumentRetriever:
    """
    Handles retrieving the most relevant context chunks for any user question.
    """
    def __init__(self, collection_name: str = "pdf_knowledge_base", db_path: str = os.path.join("data", "chroma")):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection(name=collection_name)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve(self, query: str, top_k: int = 3, distance_threshold: float = 1.5):
        """
        Retrieves the top_k most relevant chunks for a query.
        
        Args:
            query (str): The user's question.
            top_k (int): Number of chunks to retrieve (e.g. 1, 3, 5).
            distance_threshold (float): Ignore chunks with distance greater than this (filters noise).
            
        Returns:
            list[dict]: List of retrieved chunk dictionaries with text, page number, and score.
        """
        # 1. Convert question to vector embedding
        query_embedding = self.model.encode(query).tolist()

        # 2. Query ChromaDB for top_k items
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        retrieved_chunks = []
        if not results or not results["ids"] or len(results["ids"][0]) == 0:
            return retrieved_chunks

        # 3. Format and filter results
        for rank in range(len(results["ids"][0])):
            chunk_id = results["ids"][0][rank]
            doc_text = results["documents"][0][rank]
            metadata = results["metadatas"][0][rank]
            distance = results["distances"][0][rank]

            # Quality filter: If distance is too large, the chunk is irrelevant
            if distance > distance_threshold:
                continue

            retrieved_chunks.append({
                "rank": rank + 1,
                "chunk_id": chunk_id,
                "text": doc_text,
                "page_number": metadata.get("page_number", 1),
                "doc_name": metadata.get("doc_name", "unknown.pdf"),
                "distance": distance
            })

        return retrieved_chunks


def run_retrieval_demo():
    print("=" * 70)
    print("🎣 INITIALIZING RETRIEVAL ENGINE")
    print("=" * 70)

    retriever = DocumentRetriever()
    
    query = "What are the rules regarding API keys and credential leaks?"
    print(f"❓ User Question: \"{query}\"\n")

    # Experiment with different Top-K values
    for k in [1, 3, 5]:
        print("=" * 70)
        print(f"🔬 TESTING WITH Top-K = {k}")
        print("=" * 70)
        
        results = retriever.retrieve(query=query, top_k=k)
        
        for item in results:
            print(f"[{item['rank']}] 📄 Page {item['page_number']} | Distance: {item['distance']:.4f} | ID: {item['chunk_id']}")
            print(f"    Excerpt: \"{item['text'][:90]}...\"\n")

if __name__ == "__main__":
    run_retrieval_demo()
