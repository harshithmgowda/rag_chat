"""
Phase 7: LLM Integration (NVIDIA NIM / LLaMA-3 / Nemotron)
Demonstrates:
1. Loading secrets securely from .env
2. Direct LLM calls via OpenAI-compatible SDK
3. Context-augmented RAG Prompting (Grounding the LLM to only answer from context)
"""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Ensure Windows terminal outputs UTF-8 characters cleanly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load environment variables from .env file
load_dotenv()

def get_llm_client():
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    
    if not api_key or api_key.startswith("your_"):
        raise ValueError("❌ Missing NVIDIA_API_KEY in .env file!")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )
    return client


def generate_rag_answer(question: str, retrieved_context: list, model: str = None):
    """
    Sends the user question + retrieved chunks to the LLM with a strict grounding prompt.
    """
    if not model:
        model = os.getenv("LLM_MODEL", "meta/llama-3.1-70b-instruct")

    client = get_llm_client()

    # 1. Build the context block from retrieved chunks
    context_text = ""
    sources = set()
    for item in retrieved_context:
        context_text += f"\n[Document: {item['doc_name']}, Page: {item['page_number']}]\n{item['text']}\n"
        sources.add(f"Page {item['page_number']}")

    # 2. Construct the strict System Prompt
    system_prompt = (
        "You are an expert AI assistant that answers questions based STRICTLY and ONLY on the provided PDF excerpts.\n"
        "Rules you MUST follow:\n"
        "1. Answer using ONLY the information provided in the context below.\n"
        "2. If the context does not contain enough information to answer the question, say: "
        "'I couldn't find this information in the uploaded document.'\n"
        "3. Do NOT make up facts or use outside knowledge.\n"
        "4. Always cite the page number(s) where the information was found."
    )

    # 3. Construct the User Prompt with Question and Injected Context
    user_prompt = f"""
--- CONTEXT FROM UPLOADED PDF ---
{context_text}
--- END OF CONTEXT ---

USER QUESTION:
{question}
"""

    print("=" * 70)
    print("🤖 SENDING PROMPT TO LLM:")
    print(f"Model: {model}")
    print("=" * 70)

    # 4. Call the LLM
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,  # Low temperature = factual, deterministic, no creative hallucinations!
        max_tokens=500
    )

    answer = response.choices[0].message.content.strip()
    return answer, list(sources)


def run_llm_demo():
    print("=" * 70)
    print("🔐 VERIFYING API CONNECTION")
    print("=" * 70)
    
    try:
        client = get_llm_client()
        model = os.getenv("LLM_MODEL", "meta/llama-3.1-70b-instruct")
        print(f"✅ Connected to NVIDIA API at {os.getenv('NVIDIA_BASE_URL')}")
        print(f"✅ Selected Model: {model}\n")

        # Mock retrieved chunks (similar to what our Retriever returned in Phase 6)
        sample_context = [
            {
                "doc_name": "sample_document.pdf",
                "page_number": 3,
                "text": "Key Security Rules: 1. Store all secrets inside environment variables and load them via .env files. 2. All client communication must occur over HTTPS with TLS 1.3 encryption."
            },
            {
                "doc_name": "sample_document.pdf",
                "page_number": 3,
                "text": "3. Rate limiting is set to 60 requests per minute per IP. 4. In case of a credential leak, the security response team must revoke the key within 15 minutes."
            }
        ]

        question = "What is the policy for leaked credentials and what is the deadline to revoke them?"
        print(f"❓ User Question: \"{question}\"")

        answer, sources = generate_rag_answer(question, sample_context, model=model)

        print("\n" + "=" * 70)
        print("🎯 FINAL LLM RESPONSE:")
        print("=" * 70)
        print(answer)
        print("\n📚 CITED SOURCES:", ", ".join(sources))
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error during LLM call: {e}")

if __name__ == "__main__":
    run_llm_demo()
