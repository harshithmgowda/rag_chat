"""
Phase 8: Complete End-to-End CLI RAG Chatbot
Interactive terminal application where you can load ANY PDF and chat with it!
"""
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from backend.app.services.rag_service import RAGService

def start_cli():
    print("=" * 70)
    print("🤖 WELCOME TO YOUR PDF RAG CHATBOT (CLI EDITION)")
    print("=" * 70)

    rag = RAGService()

    default_pdf = "sample_document.pdf"
    print(f"\nDefault PDF available: '{default_pdf}'")
    pdf_input = input("Enter path to ANY PDF (Press Enter for default): ").strip()
    
    pdf_path = pdf_input if pdf_input else default_pdf

    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' does not exist!")
        return

    print(f"\n⚙️ Ingesting & indexing '{pdf_path}' into Vector Database...")
    try:
        stats = rag.ingest_pdf(pdf_path)
        print(f"✅ Ingestion Complete!")
        print(f"   📄 Document Name : {stats['doc_name']}")
        print(f"   📑 Total Pages   : {stats['pages_count']}")
        print(f"   🧩 Chunks Stored : {stats['chunks_count']}")
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return

    print("\n" + "=" * 70)
    print("💬 YOU CAN NOW ASK QUESTIONS ABOUT YOUR PDF!")
    print("   (Type 'exit' or 'quit' to stop)")
    print("=" * 70 + "\n")

    while True:
        try:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye! Happy RAG engineering!")
                break

            print("\n🔍 Retrieving context & thinking...")
            result = rag.ask(question, doc_name=os.path.basename(pdf_path), top_k=3)

            print("\n🤖 Bot Answer:")
            print(result["answer"])

            if result["sources"]:
                print(f"\n📚 Sources Cited: {', '.join(result['sources'])}")

            print("\n" + "-" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def run_automated_test():
    """Runs a non-interactive test with sample questions."""
    print("=" * 70)
    print("🧪 RUNNING AUTOMATED RAG PIPELINE TEST")
    print("=" * 70)
    
    rag = RAGService()
    rag.ingest_pdf("sample_document.pdf")

    test_questions = [
        "What are the states of a process in an operating system?",
        "What is the maximum allowed time to revoke a leaked credential?"
    ]

    for q in test_questions:
        print(f"\n❓ Question: {q}")
        res = rag.ask(q, doc_name="sample_document.pdf", top_k=2)
        print(f"🤖 Answer: {res['answer']}")
        print(f"📚 Sources: {', '.join(res['sources'])}")
        print("-" * 50)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_automated_test()
    else:
        start_cli()
