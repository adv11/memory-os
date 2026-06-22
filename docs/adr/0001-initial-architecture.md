# ADR 0001: Initial Architecture

## Status

Accepted for planning. Pending implementation approval.

## Context

MemoryOS needs to support production-grade growth while staying simple enough to build and validate quickly.

## Decision

Use a modular monolith backend with Spring Boot 3.x and Java 21, a Next.js frontend, PostgreSQL with Flyway migrations, and Google Drive for user-owned file storage.

Knowledge graph data will be derived dynamically from relational records in PostgreSQL. React Flow will render the graph on the frontend.

## Consequences

- The system can ship V1 without operating a graph database or AI infrastructure.
- Strong domain boundaries can still evolve into services later if needed.
- PostgreSQL remains the primary source of truth.
- AI and graph infrastructure decisions are deferred until product usage justifies them.
