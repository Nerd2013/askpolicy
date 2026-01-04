from typing import Any, Dict, List
from pydantic import BaseModel


class ChunkExplanation(BaseModel):
    doc_id: str
    chunk_index: int | None
    distance: float | None
    included: bool
    reason: str | None


class ExplanationPayload(BaseModel):
    approved: List[ChunkExplanation]
    dropped: List[ChunkExplanation]
    stats: Dict[str, Any]


class AskResponse(BaseModel):
    answer: str
    explanation: ExplanationPayload