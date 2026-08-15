"""
Phase 3: Chunking (Text Splitting Engine)
Splits raw document text into bite-sized, overlapping chunks with metadata.
"""
import sys
import os
import pymupdf

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def split_text_into_chunks(text: str, chunk_size: int = 300, chunk_overlap: int = 50):
    """
    Splits a long string into smaller overlapping chunks based on character count.
    
    Args:
        text (str): The full text to split.
        chunk_size (int): Maximum characters per chunk.
        chunk_overlap (int): Number of characters to share between consecutive chunks.
        
    Returns:
        List[str]: List of text chunks.
    """
    if not text or chunk_size <= 0:
        return []
    
    # If overlap is >= chunk_size, it would cause an infinite loop!
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly less than chunk_size!")

    chunks = []
    start = 0
    text_length = len(text)

    # Step forward by (chunk_size - chunk_overlap) on each iteration
    step = chunk_size - chunk_overlap

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        start += step

    return chunks


def process_pdf_into_chunks(pdf_path: str, chunk_size: int = 250, chunk_overlap: int = 40):
    """
    Reads a PDF and creates structured chunks containing:
    - chunk_id
    - page_number
    - chunk_text
    - char_count
    """
    doc = pymupdf.open(pdf_path)
    all_chunks = []
    global_chunk_id = 0

    print("=" * 65)
    print(f"🧩 CHUNKING PDF: {os.path.basename(pdf_path)}")
    print(f"⚙️ Config: Chunk Size = {chunk_size} chars | Overlap = {chunk_overlap} chars")
    print("=" * 65)

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_number = page_idx + 1
        page_text = page.get_text("text").strip()

        # Split the text of this specific page into chunks
        page_chunks = split_text_into_chunks(page_text, chunk_size, chunk_overlap)

        for local_idx, chunk_text in enumerate(page_chunks):
            global_chunk_id += 1
            chunk_metadata = {
                "chunk_id": f"chunk_{global_chunk_id}",
                "page_number": page_number,
                "chunk_index_in_page": local_idx + 1,
                "text": chunk_text,
                "char_count": len(chunk_text)
            }
            all_chunks.append(chunk_metadata)

            print(f"\n🔹 [{chunk_metadata['chunk_id']}] (From Page {page_number})")
            print(f"📊 Length: {chunk_metadata['char_count']} chars")
            print(f"📝 Content: \"{chunk_text[:100]}...\"" if len(chunk_text) > 100 else f"📝 Content: \"{chunk_text}\"")

    total_pages = len(doc)
    doc.close()
    print("\n" + "=" * 65)
    print(f"✅ Created {len(all_chunks)} total chunks across {total_pages} pages!")
    print("=" * 65)

    return all_chunks

def demonstrate_overlap_example():
    """
    Shows a simple visual example of how overlap prevents context loss.
    """
    sample_text = "The quick brown fox jumps over the lazy dog. Artificial Intelligence is transforming modern search."
    chunk_size = 45
    chunk_overlap = 15
    
    print("\n" + "=" * 65)
    print("🔍 VISUAL DEMO: HOW OVERLAP WORKS ON A SENTENCE")
    print("=" * 65)
    print(f"Original Text ({len(sample_text)} chars):\n\"{sample_text}\"")
    print(f"\nSettings: Chunk Size = {chunk_size} | Overlap = {chunk_overlap}\n")
    
    chunks = split_text_into_chunks(sample_text, chunk_size, chunk_overlap)
    for i, c in enumerate(chunks, 1):
        print(f"Chunk {i}: \"{c}\"")
    print("=" * 65)

if __name__ == "__main__":
    # 1. Visual demonstration of overlap
    demonstrate_overlap_example()
    
    # 2. Process our real sample PDF
    chunks = process_pdf_into_chunks("sample_document.pdf", chunk_size=250, chunk_overlap=40)
