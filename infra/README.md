# Infrastructure

Infrastructure will be added after the initial application scaffold exists.

Start with minimal production deployment requirements:

- Containerized backend.
- Managed PostgreSQL.
- Frontend hosting.
- Secret management.
- Health checks and structured logs.

## Local PostgreSQL

Use the local compose file from the repository root:

```bash
docker compose -f infra/docker/docker-compose.local.yml up -d
```
