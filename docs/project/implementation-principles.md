# Implementation Principles

## Product Principles

- Build the learning capture loop before advanced AI.
- Keep user data ownership clear.
- Make the system useful before making it intelligent.
- Prefer boring, reliable infrastructure until usage proves otherwise.

## Engineering Principles

- API-first backend design.
- Modular domain boundaries.
- User ownership checks at every data access boundary.
- Database migrations for every schema change.
- Tests for services, controllers, and critical frontend flows.
- Observability from the beginning: structured logs, request IDs, and health checks.

## Anti-Goals for V1

- No Neo4j.
- No vector database.
- No Kafka.
- No Redis.
- No GraphRAG.
- No multi-agent architecture.
- No complex AI pipeline.

