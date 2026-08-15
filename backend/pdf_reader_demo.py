"""
Phase 2: First PDF Reader (No LangChain, pure Python + PyMuPDF)
This script demonstrates how to open a PDF, iterate through pages,
and extract text along with page numbers and metadata.
"""
import pymupdf  # PyMuPDF library for fast, accurate PDF processing
import sys
import os

# Ensure Windows terminal outputs UTF-8 characters cleanly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def extract_text_from_pdf(pdf_path: str):
    """
    Opens a PDF file and extracts text page by page.
    Returns a list of dictionaries containing page number and text content.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at '{pdf_path}'")
        return []

    print("=" * 60)
    print(f"📖 OPENING PDF: {os.path.basename(pdf_path)}")
    print("=" * 60)

    # 1. Open the PDF document
    # pymupdf.open() loads the PDF into memory so we can access its pages
    doc = pymupdf.open(pdf_path)

    # Print document-level metadata
    print(f"📄 Total Pages : {len(doc)}")
    print(f"📝 Metadata    : {doc.metadata.get('format', 'PDF')}")
    print("=" * 60)

    extracted_pages = []

    # 2. Iterate through each page (0-indexed internally, we display 1-indexed for humans)
    for page_index in range(len(doc)):
        # Get the specific page object
        page = doc[page_index]
        
        # 3. Extract plain text from this page
        # get_text("text") extracts clean, readable string representation of text
        page_text = page.get_text("text").strip()
        
        page_number = page_index + 1  # 1-indexed page number

        # Store the extracted information
        page_data = {
            "page_number": page_number,
            "text": page_text,
            "char_count": len(page_text),
            "word_count": len(page_text.split())
        }
        extracted_pages.append(page_data)

        # 4. Display page extraction results
        print(f"\n--- 📄 PAGE {page_number} ---")
        print(f"📊 Stats: {page_data['word_count']} words | {page_data['char_count']} characters")
        print("--- CONTENT PREVIEW ---")
        print(page_text)
        print("-" * 40)

    # 5. Close the document to free memory
    doc.close()

    print("\n" + "=" * 60)
    print(f"✅ Extracted text from {len(extracted_pages)} page(s) successfully!")
    print("=" * 60)

    return extracted_pages

if __name__ == "__main__":
    # Test with our sample document
    sample_pdf = "sample_document.pdf"
    pages = extract_text_from_pdf(sample_pdf)
