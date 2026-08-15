"""
Phase 4: Embeddings & Semantic Similarity
Demonstrates turning text into numerical vectors and measuring semantic similarity
using Cosine Similarity from scratch.
"""
import sys
import os
import math
import numpy as np
from sentence_transformers import SentenceTransformer

# Ensure Windows terminal outputs UTF-8 characters cleanly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def cosine_similarity_manual(vec1: list, vec2: list) -> float:
    """
    Computes Cosine Similarity between two vectors from pure scratch.
    
    Formula:
        Cosine Similarity = (A . B) / (||A|| * ||B||)
        
        Where:
        - (A . B) is the Dot Product (sum of element-wise multiplication)
        - ||A|| is the Euclidean Norm (square root of sum of squares)
    """
    # 1. Calculate Dot Product: sum(a_i * b_i)
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # 2. Calculate Magnitudes (Norms)
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))

    # Prevent division by zero
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    # 3. Divide dot product by product of magnitudes
    return dot_product / (norm_a * norm_b)


def run_embedding_demo():
    print("=" * 70)
    print("🧠 LOADING EMBEDDING MODEL: all-MiniLM-L6-v2")
    print("=" * 70)
    
    # Load the popular lightweight embedding model (produces 384 numbers per text)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Model loaded into memory successfully!\n")

    # Sample sentences to demonstrate semantic similarity
    sentences = [
        "I like dogs",
        "I love puppies",
        "I repaired my computer"
    ]

    print("=" * 70)
    print("🔢 CONVERTING SENTENCES INTO VECTORS (EMBEDDINGS)")
    print("=" * 70)

    # Generate embeddings
    embeddings = model.encode(sentences)

    for idx, (sentence, vector) in enumerate(zip(sentences, embeddings), 1):
        print(f"\nSentence {idx}: \"{sentence}\"")
        print(f"📊 Vector Dimensions: {len(vector)} numbers")
        # Display the first 5 numbers as a preview
        preview = [round(float(n), 4) for n in vector[:5]]
        print(f"📍 First 5 coordinates: {preview} ...")

    print("\n" + "=" * 70)
    print("📐 CALCULATING COSINE SIMILARITY (SEMANTIC DISTANCE)")
    print("=" * 70)

    sim_1_2 = cosine_similarity_manual(embeddings[0], embeddings[1])
    sim_1_3 = cosine_similarity_manual(embeddings[0], embeddings[2])

    print(f"\n1️⃣ \"{sentences[0]}\"  VS  2️⃣ \"{sentences[1]}\"")
    print(f"   Similarity Score: {sim_1_2:.4f} (Very close in meaning! 🐕)")

    print(f"\n1️⃣ \"{sentences[0]}\"  VS  3️⃣ \"{sentences[2]}\"")
    print(f"   Similarity Score: {sim_1_3:.4f} (Completely unrelated topic! 💻)")

    print("\n" + "=" * 70)
    print("🔎 TESTING SEMANTIC SEARCH ON PDF CHUNKS")
    print("=" * 70)

    # Let's test with 3 sample chunks from our PDF
    chunks = [
        "Artificial Intelligence (AI) has revolutionized how humans interact with technology. Large Language Models...",
        "An Operating System (OS) manages hardware resources. Process States: Ready, Running, Waiting. Virtual Memory uses paging.",
        "Store all secrets inside environment variables and load them via .env files. Never commit API keys."
    ]

    chunk_embeddings = model.encode(chunks)

    # User Query
    user_query = "How does CPU handle running processes and memory paging?"
    print(f"❓ User Query: \"{user_query}\"\n")
    query_vector = model.encode(user_query)

    print("Comparing query against each chunk:\n")
    for i, (chunk, chunk_vec) in enumerate(zip(chunks, chunk_embeddings), 1):
        score = cosine_similarity_manual(query_vector, chunk_vec)
        print(f"Chunk {i} Similarity: {score:.4f} -> \"{chunk[:65]}...\"")

    print("=" * 70)
    print("🎯 Notice how Chunk 2 received the highest score automatically!")
    print("=" * 70)

if __name__ == "__main__":
    run_embedding_demo()
