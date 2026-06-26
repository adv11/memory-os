# ADR 0001: Initial Architecture

## Status

Accepted and implemented (Phase 1 complete).

## Context

MemoryOS needs to support production-grade growth while staying simple enough to build and validate quickly. The initial architecture decision was made before any code was written.

## Decision

Use a modular monolith backend with Python 3.9+ and FastAPI, a Next.js frontend, PostgreSQL with Alembic migrations, and Google Drive for user-owned file storage.

Python was chosen because the roadmap includes RAG, LLMs, and agentic AI workflows. Python has the best ecosystem for all of these. FastAPI is async-first and generates OpenAPI docs automatically.

Knowledge graph data will be derived dynamically from relational records in PostgreSQL. React Flow will render the graph on the frontend.

## Consequences

- The system ships V1 without a graph database or AI infrastructure.
- Domain boundaries inside the monolith can evolve into separate services later without a rewrite.
- PostgreSQL is the single source of truth.
- AI and graph infrastructure decisions are deferred until product usage justifies them.
- Python's async ecosystem (FastAPI + SQLAlchemy async + asyncpg) gives the performance needed for future AI workloads without changing the runtime.

## Full design

See `docs/architecture/architecture.md` for the complete system design, flows, and diagrams.
