# MemoryOS

A personal learning memory system. Capture what you learn, organise it by topic, attach resources, and visualise your knowledge growth.

**Start here → [docs/PROJECT.md](docs/PROJECT.md)**

That file explains what is built, what the words mean, how to run it locally, and where everything lives.

---

## Quick start

```bash
# 1. Start PostgreSQL
docker compose -f infra/docker/docker-compose.local.yml up -d

# 2. Configure and run backend (fill in Google credentials in .env first)
cp services/backend/.env.example services/backend/.env
cd services/backend && export $(cat .env | xargs) && mvn spring-boot:run

# 3. Run frontend (separate terminal)
cd apps/frontend && npm install && npm run dev
```

Frontend: http://localhost:3000 — Backend: http://localhost:8080

For Google OAuth setup and full instructions see [docs/project/setup.md](docs/project/setup.md).

---

## Stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: Spring Boot 3.x, Java 25, Spring Security, OAuth2
- Database: PostgreSQL, Flyway
- File storage: Google Drive API (planned)
- Graph: React Flow (planned)

## Rule

Start simple. Ship the core learning capture workflow first. Do not add Neo4j, vector databases, Kafka, Redis, or AI pipelines until real production usage justifies them.
