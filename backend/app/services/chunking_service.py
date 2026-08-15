"""
Chunking Service
Splits raw text pages into overlapping chunks with precise metadata.
"""

def split_text_into_chunks(text: str, chunk_size: int = 350, chunk_overlap: int = 50) -> list[str]:
    """
    Sliding window chunking based on character length with safety checks.
    """
    if not text or chunk_size <= 0:
        return []
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly less than chunk_size")

    chunks = []
    start = 0
    step = chunk_size - chunk_overlap
    text_len = len(text)

    while start < text_len:
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step

    return chunks


def chunk_extracted_pages(pages_data: list[dict], chunk_size: int = 350, chunk_overlap: int = 50) -> list[dict]:
    """
    Processes a list of extracted pages into structured chunks.
    
    Returns:
        list[dict]: List of chunk dictionaries containing chunk_id, text, page_number, and doc_name.
    """
    all_chunks = []
    global_chunk_count = 0

    for page in pages_data:
        page_chunks = split_text_into_chunks(page["text"], chunk_size, chunk_overlap)
        
        for local_idx, chunk_text in enumerate(page_chunks):
            global_chunk_count += 1
            all_chunks.append({
                "chunk_id": f"{page['doc_name']}_p{page['page_number']}_c{local_idx + 1}",
                "text": chunk_text,
                "page_number": page["page_number"],
                "doc_name": page["doc_name"],
                "char_count": len(chunk_text)
            })

    return all_chunks
