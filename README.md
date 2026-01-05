# AskPolicy — Explainable, Auditable RAG System

## Overview
AskPolicy is a production-grade, explainable Retrieval-Augmented Generation (RAG) system for answering questions over company policy documents.

It is designed with **trust, auditability, and replay** as first-class concerns — not afterthoughts.

---

## Core Capabilities

- Multi-document ingestion (PDFs)
- Deterministic RAG pipeline (via `rag-core`)
- Policy-driven context selection
- Explainable answers (why an answer was produced)
- Audit-safe persistence (append-only history)
- Deterministic replay of past questions
- Answer and context diffing across replays

---

## High-Level Architecture

```
           ┌────────────┐
           │  Ask UI    │   (User-facing)
           └─────┬──────┘
                 │
           ┌─────▼──────┐
           │ AskPolicy  │   FastAPI
           │   API      │
           └─────┬──────┘
                 │
   ┌─────────────▼─────────────┐
   │        rag-core             │
   │  (Reusable RAG Engine)      │
   │                             │
   │  • Retrieval                │
   │  • Context Policy           │
   │  • Answer Generation        │
   │  • Claim Verification       │
   │  • Entailment Checking      │
   └─────────────┬─────────────┘
                 │
        ┌────────▼────────┐
        │  SQLite Audit   │
        │  (Append-only)  │
        └────────┬────────┘
                 │
    ┌────────────▼────────────┐
    │ Monitoring / History UI │
    │  • Explainability       │
    │  • Replay               │
    │  • Diff View            │
    └─────────────────────────┘
```

---

## Design Principles

- **Separation of concerns**
  - `rag-core` is a reusable library
  - AskPolicy is an application
  - UIs never import RAG internals

- **Audit-first**
  - Every interaction is persisted
  - Original records are immutable
  - Replays create new records

- **Failure-safe**
  - Persistence failures never block answers
  - Replay never overwrites history

- **Explainability**
  - Approved and dropped context is visible
  - Raw chunk text is inspectable
  - Policy decisions are explicit

---

## User Interfaces

- **Ask UI**
  - Simple question → answer
  - No internal details exposed

- **Monitoring UI**
  - Inspect approved/dropped chunks
  - View distances and raw chunk text
  - Debug retrieval and policy behavior

- **History & Replay UI**
  - View past interactions
  - Replay questions against current documents
  - Compare answers and context diffs

---

## What This Project Demonstrates

- Production-grade RAG architecture
- Deterministic, testable LLM usage
- Explainability beyond basic citations
- Audit and compliance readiness
- Enterprise-style replay and diffing

This system is **not a demo** — it is a reference-quality implementation.

---

## Status

**Frozen.**  
All core functionality is complete and stable.

Future work (intentionally deferred):
- Authentication
- Deployment automation
- User-level access control
