"""
Utility script to create a clean, multi-page sample PDF for testing our RAG pipeline.
"""
import fitz  # PyMuPDF
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def create_sample_pdf(output_path: str = "sample_document.pdf"):
    doc = fitz.open()
    
    # Page 1: Introduction to AI & Retrieval Systems
    page1 = doc.new_page()
    page1_text = (
        "AI & Retrieval Systems Handbook\n"
        "Page 1: Introduction to Modern Artificial Intelligence\n\n"
        "Artificial Intelligence (AI) has revolutionized how humans interact with technology. "
        "Large Language Models (LLMs), such as GPT-4 and Llama 3, are deep learning models trained "
        "on vast amounts of textual data. They excel at understanding grammar, summarizing documents, "
        "and answering general knowledge inquiries.\n\n"
        "However, LLMs suffer from two major limitations:\n"
        "1. Knowledge Cutoff: An LLM only knows information up to its training date.\n"
        "2. Hallucinations: When an LLM does not know a specific fact, it may fabricate a plausible-sounding answer.\n\n"
        "To solve this, Retrieval-Augmented Generation (RAG) was introduced. RAG connects an LLM to external "
        "private databases, allowing the model to look up verified facts before speaking."
    )
    page1.insert_text((50, 72), page1_text, fontsize=11, fontname="helv")
    
    # Page 2: Operating Systems & Process Scheduling
    page2 = doc.new_page()
    page2_text = (
        "AI & Retrieval Systems Handbook\n"
        "Page 2: Operating Systems Fundamentals\n\n"
        "An Operating System (OS) manages hardware resources and provides common services for programs. "
        "The core component of an OS is the Kernel. A Process is an executing instance of a computer program.\n\n"
        "Process States:\n"
        "- Ready: The process is waiting to be assigned to a CPU core.\n"
        "- Running: Instructions are actively being executed by the processor.\n"
        "- Waiting/Blocked: The process is waiting for an I/O event or signal.\n\n"
        "Virtual Memory is a memory management technique that provides an idealized abstraction of storage. "
        "It uses Paging to divide physical memory into fixed-size blocks called Frames and virtual memory into Pages. "
        "When a requested page is not in physical RAM, a Page Fault occurs."
    )
    page2.insert_text((50, 72), page2_text, fontsize=11, fontname="helv")

    # Page 3: Company Security & Cloud Infrastructure
    page3 = doc.new_page()
    page3_text = (
        "AI & Retrieval Systems Handbook\n"
        "Page 3: Cloud Infrastructure & API Security Policy\n\n"
        "All engineers must adhere to strict API security guidelines when deploying cloud services. "
        "API keys, database credentials, and access tokens must NEVER be hardcoded into source code or Git repositories.\n\n"
        "Key Security Rules:\n"
        "1. Store all secrets inside environment variables and load them via .env files.\n"
        "2. All client communication must occur over HTTPS with TLS 1.3 encryption.\n"
        "3. Rate limiting is set to a maximum of 60 requests per minute per IP address.\n"
        "4. In case of a credential leak, the security response team must revoke the key within 15 minutes."
    )
    page3.insert_text((50, 72), page3_text, fontsize=11, fontname="helv")

    doc.save(output_path)
    doc.close()
    print(f"✅ Created sample PDF successfully at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_sample_pdf("sample_document.pdf")
