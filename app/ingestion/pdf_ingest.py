from typing import Dict, List

from pypdf import PdfReader


def ingest_pdf(
    *,
    path: str,
    doc_id: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[Dict]:
    """
    Load a PDF and split it into overlapping text chunks.

    Returns chunks compatible with rag-core retrieval.
    """

    reader = PdfReader(path)
    chunks: List[Dict] = []

    chunk_index = 0

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": {
                            "doc_id": doc_id,
                            "page": page_number,
                            "chunk_index": chunk_index,
                        },
                    }
                )
                chunk_index += 1

            start += chunk_size - overlap

    return chunks