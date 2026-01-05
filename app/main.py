from fastapi import FastAPI
import logging
from rag_core import answer_query
from rag_core.policies.context_policy import ContextPolicy

from app.ingestion.pdf_ingest import ingest_pdf
from app.retrieval.policy_retriever import PolicyRetriever
from app.llm.openai_llm import OpenAILLM
from rag_core.validation.entailment import KeywordEntailmentChecker
from rag_core.pipeline.answer_query import answer_query_with_context
from app.persistence.store import init_db, store_interaction

from app.ingestion.document_loader import load_documents_from_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger("askpolicy")

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
init_db()

chunks = load_documents_from_dir(data_dir="data")
logger.info(
    "Loaded %d chunks from %d documents",
    len(chunks),
    len({c["metadata"]["doc_id"] for c in chunks}),
)

retriever = PolicyRetriever(chunks=chunks)
llm = OpenAILLM()

context_policy = ContextPolicy(
    max_chunks=5,
    min_chunks=1,
)

entailment_checker = KeywordEntailmentChecker()
# --- API ---

@app.post("/ask")
def ask(q: str):
    answer, context_pack = answer_query_with_context(
        query=q,
        retriever=retriever,
        llm=llm,
        context_policy=context_policy,
        entailment_checker=entailment_checker,
    )

    explanation = build_explanation(context_pack)

    try:
        store_interaction(
            question=q,
            answer=answer,
            explanation=explanation,
        )
    except Exception as e:
        logger.warning("Failed to persist interaction: %s", e)
    
    return {
        "answer": answer,
        "explanation": explanation,
    }
    
    
#-------------------helper ----------#
def build_explanation(context_pack):
    approved = []
    for c in context_pack.approved_chunks:
        approved.append({
            "doc_id": c["metadata"].get("doc_id"),
            "chunk_index": c["metadata"].get("chunk_index"),
            "distance": c.get("distance"),
            "included": True,
            "reason": c.get("_reason"),
            "text": c.get("text", ""),
        })

    dropped = []
    for c in context_pack.dropped_chunks:
        dropped.append({
            "doc_id": c["metadata"].get("doc_id"),
            "chunk_index": c["metadata"].get("chunk_index"),
            "distance": c.get("distance"),
            "included": False,
            "reason": c.get("_drop_reason"),
        })

    return {
        "approved": approved,
        "dropped": dropped,
        "stats": context_pack.stats,
    }