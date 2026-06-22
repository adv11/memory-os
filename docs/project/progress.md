# Progress

This file is the living implementation memory for MemoryOS. Update it whenever a meaningful decision is made, a phase starts, or a feature is completed.

## Current Phase

Phase 1: Authentication.

## Completed

- Created initial project documentation structure.
- Captured product vision, target users, stack, and V1 scope.
- Defined architecture docs required before implementation.
- Architecture package approved for V1.
- Scaffolded Spring Boot backend with Java 25 target and Maven.
- Added Spring Security OAuth2 Login configuration for Google.
- Added authenticated user provisioning and persistence.
- Added `/api/v1/me` current-user endpoint.
- Added Flyway migration `V1__create_identity.sql`.
- Added backend identity provisioning tests.
- Scaffolded Next.js frontend with TypeScript and Tailwind CSS.
- Added login/logout links wired to backend OAuth routes.
- Added browser-side authenticated dashboard state handling.
- Added local development documentation and env examples.
- Added local PostgreSQL Docker Compose setup.
- Updated frontend dependency tree to clear npm audit findings.
- Verified local PostgreSQL Docker Compose starts and backend connects successfully.
- Flyway V1 migration confirmed applied on first backend startup.
- Created `docs/PROJECT.md` single start-here project guide.
- Created `.amazonq/rules/agent-rules.md` AI agent instruction file.
- Created `docs/explainers/google-auth.md` deep-dive explainer for auth feature.
- Removed redundant `db/` root directory.
- Fixed `loginUrl` in frontend `config.ts` (wrong Spring Security path).
- Added generic exception fallback handler to `GlobalExceptionHandler`.
- Updated `infra/README.md` to reflect actual Docker Compose setup.
- Updated `docs/architecture/folder-structure.md` to show current vs planned layout.
- Created `docs/explainers/README.md` explainers index.
- Fixed run command across all docs to use `export $(cat .env | xargs) && mvn spring-boot:run`.
- Added Google OAuth credential setup steps to `local-development.md`.
- Removed stale `db/migrations/README.md` reference from agent-rules.
- Consolidated architecture docs: merged high-level-architecture, low-level-architecture, sequence-diagrams, google-drive-integration, knowledge-graph-visualization into single `docs/architecture/architecture.md`.
- Renamed `api-contracts.md` → `api.md`.
- Deleted `folder-structure.md` (content merged into PROJECT.md and architecture.md).
- Renamed `local-development.md` → `setup.md` with clearer step-by-step format.
- Deleted `implementation-principles.md` (content merged into agent-rules.md).
- Deleted `glossary.md` (content merged into PROJECT.md).
- Deleted `docs/product/product-requirements.md` (content merged into PROJECT.md).
- Rewrote root README.md to be minimal and point to PROJECT.md.
- Updated ADR 0001 status to accepted and implemented.
- Added integration test rules and naming conventions to agent-rules.md.

## In Progress

- Phase 1 local OAuth credential setup and manual browser verification (Google credentials not yet configured).

## Not Started

- Topic management.
- Learning session management.
- Resource metadata management.
- Google Drive integration.
- Concept management.
- Knowledge graph visualization.
- Dashboard.

## Blockers

- Manual OAuth login cannot be completed until Google OAuth credentials are configured.

## Validation

| Date | Check | Result |
| --- | --- | --- |
| 2026-06-22 | `mvn clean test` in `services/backend` with JDK 25 | Passed: 2 tests, 0 failures. |
| 2026-06-22 | `npm run typecheck` in `apps/frontend` | Passed. |
| 2026-06-22 | `npm run build` in `apps/frontend` | Passed. |
| 2026-06-22 | `npm audit --audit-level=moderate` in `apps/frontend` | Passed: 0 vulnerabilities. |
| 2026-06-22 | Docker Compose PostgreSQL startup and backend DB connection | Passed: HikariPool connected, Flyway applied V1 migration. |

## Decision Log

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-06-22 | Use PostgreSQL for V1 graph data | Simpler operations and enough for dynamic graph visualization. |
| 2026-06-22 | Use Google Drive for user-owned file storage | Keeps files under user ownership and avoids operating storage infrastructure early. |
| 2026-06-22 | Defer AI, vector DBs, Neo4j, Kafka, Redis | Avoid premature complexity before product-market proof. |
| 2026-06-22 | Use Maven for the backend scaffold | Available locally and fits Spring Boot conventions. |
| 2026-06-22 | Pin Next.js to 16.2.9 with a PostCSS override | Clears known npm audit advisories in the frontend tree. |
