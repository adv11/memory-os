# Infrastructure

## What exists now

### Local PostgreSQL (Docker Compose)

Start it from the repo root:

```bash
docker compose -f infra/docker/docker-compose.local.yml up -d
```

This starts a PostgreSQL 16 container with:
- Container name: `memoryos-postgres`
- Port: `5432` (mapped to host)
- Database: `memoryos`
- Username: `memoryos`
- Password: `memoryos`
- Data persisted in a named Docker volume: `memoryos_postgres_data`

Stop it:
```bash
docker compose -f infra/docker/docker-compose.local.yml down
```

Wipe all data (useful for a clean slate):
```bash
docker compose -f infra/docker/docker-compose.local.yml down -v
```

Check it is ready:
```bash
docker exec memoryos-postgres pg_isready -U memoryos -d memoryos
```

## What is planned for production

- Containerised Spring Boot backend (Dockerfile to be added).
- Managed PostgreSQL (AWS RDS, Supabase, or similar).
- Frontend on Vercel or containerised Next.js.
- Secret management via cloud provider (AWS Secrets Manager or environment variables in the deployment platform).
- Health checks wired to the Spring Boot Actuator endpoint at `/actuator/health`.

None of this is implemented yet. Add it when deployment requirements become concrete.
