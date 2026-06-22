# MemoryOS — Project Guide

This is the one file to read first. It tells you what the project is, what the words mean, what is built, and where everything lives. You do not need to explore the whole repo to get started.

---

## What is MemoryOS?

MemoryOS is a personal learning memory system. It helps people who are learning multiple subjects at once — engineers, students, interview preppers — capture what they learn, organise it, and eventually use AI to help them retain it.

It is not a general note-taking app. The goal is an AI-powered memory operating system that understands what a user has learned and helps them not forget it.

**Target users:** software engineers, students, interview preparation candidates, competitive exam aspirants, lifelong learners.

---

## Words used in this project

**Topic** — a broad learning area a user is studying. Examples: DSA, System Design, Spring Boot, Machine Learning.

**Learning Session** — a record of what a user learned on a specific day under a topic. It has a title, description, difficulty score (1–10), date, resources, and concepts.

**Resource** — a file or link attached to a learning session. Files are stored in the user's Google Drive. MemoryOS stores the metadata and the Drive file ID.

**Concept** — an important idea captured from a learning session. Examples: Class Diagram, Binary Search, Eventual Consistency.

**Knowledge Graph** — a visual map of relationships between topics, sessions, and concepts. In V1 it is built dynamically from PostgreSQL data using React Flow.

**Revision Engine** — a future feature for spaced repetition and adaptive review scheduling. Not in V1.

**Knowledge Decay** — a future estimate of what the user might be forgetting. Not in V1.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Backend | Spring Boot 3.x, Java 25, Spring Security |
| Auth | Google OAuth2 (Spring Security OAuth2 Login) |
| Database | PostgreSQL 16, Flyway migrations |
| File storage | Google Drive API (Phase 4) |
| Graph UI | React Flow (Phase 6) |

---

## What is built right now (Phase 1 complete)

- Google OAuth login. Users sign in with Google, no passwords.
- On first login, a user record is created in PostgreSQL (`app_user` table).
- On subsequent logins, the profile (email, name) is updated if changed.
- `GET /api/v1/me` returns the authenticated user's profile.
- Frontend has a landing page, login button, and a dashboard shell.
- Local PostgreSQL runs via Docker Compose.
- Flyway manages all schema migrations. `V1__create_identity.sql` has been applied.

## What is NOT built yet

- Topic management (Phase 2)
- Learning sessions (Phase 3)
- Resource attachments and Google Drive upload (Phase 4)
- Concept management (Phase 5)
- Knowledge graph visualization (Phase 6)
- Dashboard metrics (Phase 7)
- AI revision engine (future)

---

## Repository layout

```
memory-os/
  apps/
    frontend/          Next.js web app
  services/
    backend/           Spring Boot API
  infra/
    docker/            Local PostgreSQL Docker Compose
  docs/
    architecture/      System design and API contracts (start with architecture.md)
    adr/               Architecture Decision Records
    explainers/        Deep-dive feature explainers
    project/           Setup guide, progress log, todo list
  .amazonq/
    rules/             Instructions for AI agents
```

---

## Backend package structure

```
com.memoryos/
  MemoryOsApplication.java
  common/
    api/          ApiPaths.java            — all API path constants live here
    error/        GlobalExceptionHandler, ApiErrorResponse
    security/     SecurityConfig, CorsProperties, WebProperties
  identity/
    controller/   MeController             — GET /api/v1/me
    service/      AuthenticatedUserService, OAuthUserProvisioningService
    repository/   AppUserRepository
    entity/       AppUser
    dto/          CurrentUserResponse
```

Each future domain (topics, sessions, resources, concepts, graph, dashboard) adds one package following the same `controller / service / repository / entity / dto` structure.

---

## Database schema (current)

```sql
app_user (
  id           UUID PRIMARY KEY,
  google_id    VARCHAR(128) UNIQUE NOT NULL,   -- Google's stable "sub" claim
  email        VARCHAR(320) UNIQUE NOT NULL,
  name         VARCHAR(200) NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL,
  updated_at   TIMESTAMPTZ NOT NULL
)
```

Migrations live in: `services/backend/src/main/resources/db/migration/`

Flyway runs them automatically on startup. Naming format: `V{number}__{description}.sql`

To see which migrations have run:
```bash
docker exec -it memoryos-postgres psql -U memoryos -d memoryos -c "SELECT * FROM flyway_schema_history;"
```

---

## How to run locally

See `docs/project/setup.md` for the full step-by-step guide.

Quick version:
```bash
# 1. Start PostgreSQL
docker compose -f infra/docker/docker-compose.local.yml up -d

# 2. Set up and run backend (fill in Google credentials in .env first)
cp services/backend/.env.example services/backend/.env
cd services/backend && export $(cat .env | xargs) && mvn spring-boot:run

# 3. Run frontend (separate terminal)
cd apps/frontend && npm install && npm run dev
```

---

## Key URLs when running locally

| URL | What it is |
|---|---|
| http://localhost:3000 | Frontend landing page |
| http://localhost:3000/dashboard | Dashboard (requires login) |
| http://localhost:8080/login/oauth2/authorization/google | Starts Google login |
| http://localhost:8080/api/v1/me | Returns current user JSON |
| http://localhost:8080/actuator/health | Backend health check |
| http://localhost:8080/logout | Logs out |

---

## Where to read more

| What you want to know | Where to look |
|---|---|
| Full system design, flows, diagrams | `docs/architecture/architecture.md` |
| All API endpoints with request/response shapes | `docs/architecture/api.md` |
| Database tables and relationships | `docs/architecture/architecture.md` (sequence flows section) |
| How a specific feature works in depth | `docs/explainers/` |
| What to build next | `docs/project/todo.md` |
| What has been built and key decisions | `docs/project/progress.md` |
| How to set up locally | `docs/project/setup.md` |
| Rules for AI agents | `.amazonq/rules/agent-rules.md` |
