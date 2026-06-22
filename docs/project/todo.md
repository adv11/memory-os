# TODO

This file tracks executable work. Keep it synced with implementation so completed work is not repeated.

## Phase 0: Architecture Approval

- [x] Create project documentation structure.
- [x] Create high-level architecture.
- [x] Create low-level architecture.
- [x] Create database ER diagram.
- [x] Create API contracts.
- [x] Create folder structure.
- [x] Create sequence diagrams.
- [x] Create Google Drive integration design.
- [x] Create knowledge graph visualization design.
- [x] Review and approve architecture.

## Phase 1: Authentication

- [x] Scaffold Spring Boot backend.
- [x] Configure Java 25, Spring Boot 3.x, Maven.
- [x] Add Spring Security OAuth2 Login.
- [x] Configure Google OAuth client placeholders.
- [x] Persist authenticated users.
- [x] Add authenticated user profile endpoint.
- [x] Add backend authentication tests.
- [x] Scaffold Next.js frontend.
- [x] Add login/logout UI.
- [x] Add frontend auth state handling.
- [x] Add local development docs and env examples.
- [x] Add local PostgreSQL Docker Compose setup.
- [x] Run backend tests.
- [x] Run frontend typecheck, build, and audit.
- [ ] Configure real Google OAuth credentials locally.
- [ ] Manually verify browser login flow against local backend/frontend.

## Phase 2: Topic Management

- [ ] Create topic table migration.
- [ ] Implement topic entity, repository, service, and controller.
- [ ] Add create/list/update/delete topic APIs.
- [ ] Add backend tests.
- [ ] Build frontend topic list and create/edit/delete flows.

## Phase 3: Learning Sessions

- [ ] Create learning session table migration.
- [ ] Implement session entity, repository, service, and controller.
- [ ] Add session APIs scoped by topic and user.
- [ ] Add difficulty validation.
- [ ] Build frontend session creation and listing.

## Phase 4: Resource Metadata and Google Drive

- [ ] Create resource table migration.
- [ ] Implement resource metadata APIs.
- [ ] Implement Google Drive upload flow.
- [ ] Store Google Drive file IDs and metadata.
- [ ] Add upload and link-resource UI.

## Phase 5: Concept Management

- [ ] Create concept table migration.
- [ ] Implement concept APIs.
- [ ] Build concept entry UI inside learning sessions.

## Phase 6: Knowledge Graph

- [ ] Create graph API that derives nodes and edges from PostgreSQL data.
- [ ] Build React Flow graph view.
- [ ] Add time filters.
- [ ] Add node click behavior.

## Phase 7: Dashboard

- [ ] Create topic summary API.
- [ ] Show total sessions, concepts, resources, and activity timeline.

## Future Phases

- [ ] Revision engine.
- [ ] AI question generation.
- [ ] Semantic linking.
- [ ] AI tutor.
- [ ] Knowledge decay tracking.
