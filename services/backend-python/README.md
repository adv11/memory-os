# Backend (Python)

FastAPI backend for MemoryOS.

## Stack

- Python 3.9+
- FastAPI — web framework
- SQLAlchemy 2.0 async — ORM
- Authlib — Google OAuth2 client
- Starlette SessionMiddleware — server-side sessions
- asyncpg — PostgreSQL async driver
- Alembic — future database migrations
- pytest + pytest-asyncio — tests

## Structure

```
app/
  main.py              FastAPI app, middleware, routers wired together
  common/
    config.py          All env vars via pydantic-settings
    errors.py          Error response format and exception handlers
  db/
    session.py         Async SQLAlchemy engine and session factory
  identity/
    model.py           AppUser SQLAlchemy model (maps to app_user table)
    repository.py      All DB queries for app_user
    schemas.py         Pydantic request/response models
    router.py          Auth routes and /api/v1/me endpoint
tests/
  conftest.py          In-memory SQLite DB fixture
  test_identity.py     Repository and integration tests
```

## Setup

```bash
cp .env.example .env
# Fill in GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cd services/backend-python
source .venv/bin/activate && python run.py
```

Or directly:
```bash
uvicorn app.main:app --reload --port 8080
```

Make sure PostgreSQL is running first:
```bash
docker compose -f infra/docker/docker-compose.local.yml up -d
```

## Test

```bash
ENV_FILE=.env.test python -m pytest tests/ -v
```

No real PostgreSQL or Google credentials needed for tests. Uses SQLite in-memory.

## Key URLs

| URL | What it does |
|---|---|
| `GET /auth/google` | Starts Google login |
| `GET /auth/google/callback` | Google redirects here after consent |
| `GET /api/v1/me` | Returns current user (requires session) |
| `GET /logout` | Clears session, redirects to frontend |
| `GET /health` | Health check |
| `GET /docs` | Auto-generated OpenAPI docs (FastAPI built-in) |
