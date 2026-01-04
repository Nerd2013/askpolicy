from pathlib import Path
from typing import Dict, List

from app.ingestion.pdf_ingest import ingest_pdf


def load_documents_from_dir(
    *,
    data_dir: str = "data",
) -> List[Dict]:
    """
    Load and chunk all PDF documents in a directory.

    Each PDF becomes a logical document identified by its filename.
    """

    all_chunks: List[Dict] = []

    for pdf_path in Path(data_dir).glob("*.pdf"):
        doc_id = pdf_path.stem  # filename without extension

        chunks = ingest_pdf(
            path=str(pdf_path),
            doc_id=doc_id,
        )

        all_chunks.extend(chunks)

    return all_chunks