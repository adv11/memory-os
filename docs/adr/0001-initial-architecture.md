# ADR 0001: Initial Architecture

## Status

Accepted and implemented (Phase 1 complete).

## Context

MemoryOS needs to support production-grade growth while staying simple enough to build and validate quickly. The initial architecture decision was made before any code was written.

## Decision

Use a modular monolith backend with Spring Boot 3.x and Java 25, a Next.js frontend, PostgreSQL with Flyway migrations, and Google Drive for user-owned file storage.

Knowledge graph data will be derived dynamically from relational records in PostgreSQL. React Flow will render the graph on the frontend.

## Consequences

- The system ships V1 without a graph database or AI infrastructure.
- Domain boundaries inside the monolith can evolve into separate services later without a rewrite.
- PostgreSQL is the single source of truth.
- AI and graph infrastructure decisions are deferred until product usage justifies them.

## Full design

See `docs/architecture/architecture.md` for the complete system design, flows, and diagrams.
