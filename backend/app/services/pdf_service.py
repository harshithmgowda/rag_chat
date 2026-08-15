"""
PDF Extraction Service
Extracts text and page metadata from any uploaded PDF file using PyMuPDF.
"""
import os
import pymupdf

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extracts text page-by-page from any PDF file.
    
    Returns:
        list[dict]: List of dictionaries containing page_number, text, and doc_name.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    doc_name = os.path.basename(pdf_path)
    pages_data = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text("text").strip()
        
        # Only include pages that have extractable text
        if text:
            pages_data.append({
                "page_number": page_idx + 1,
                "text": text,
                "doc_name": doc_name
            })

    doc.close()
    return pages_data
