# pylint: disable=no-value-for-parameter
from typing import Dict, List

import faiss
import numpy as np
import openai


class PolicyRetriever:
    """
    FAISS-based retriever for policy documents.
    """

    def __init__(
        self,
        *,
        chunks: List[Dict],
        embedding_model: str = "text-embedding-3-small",
    ):
        self.chunks = chunks
        self.embedding_model = embedding_model

        self.embeddings = self._embed_chunks([c["text"] for c in chunks])
        self.index = self._build_index(self.embeddings)

    def _embed_chunks(self, texts: List[str]) -> np.ndarray:
        response = openai.embeddings.create(
            model=self.embedding_model,
            input=texts,
        )
        vectors = [item.embedding for item in response.data]
        return np.array(vectors).astype("float32")

    def _build_index(self, embeddings: np.ndarray):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings) # pylint: disable=no-value-for-parameter
        return index

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> List[Dict]:
        query_vec = self._embed_chunks([query])
        distances, indices = self.index.search(query_vec, k)  # pylint: disable=no-value-for-parameter
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            chunk = self.chunks[idx]
            results.append(
                {
                    "text": chunk["text"],
                    "distance": float(dist),
                    "metadata": chunk["metadata"],
                }
            )

        return results