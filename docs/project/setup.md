# Local Setup

Everything you need to run MemoryOS on your machine.

---

## What you need installed

- Python 3.9+
- pip
- Node.js 22+
- npm 11+
- Docker (for the local PostgreSQL container)
- A Google account (to create OAuth credentials)

---

## Step 1 — Get Google OAuth credentials

You need these before the backend will start.

1. Go to https://console.cloud.google.com/apis/credentials
2. Create a project (or select an existing one).
3. Click "Create Credentials" → "OAuth client ID".
4. Application type: **Web application**.
5. Under "Authorised redirect URIs" add: `http://localhost:8080/auth/google/callback`
6. Copy the **Client ID** and **Client Secret**.
7. Go to "OAuth consent screen" → set to External → add your own email as a test user.

---

## Step 2 — Start PostgreSQL

Run from the repo root:

```bash
docker compose -f infra/docker/docker-compose.local.yml up -d
```

Verify it is ready:

```bash
docker exec memoryos-postgres pg_isready -U memoryos -d memoryos
```

You should see: `localhost:5432 - accepting connections`

---

## Step 3 — Configure the backend

```bash
cp services/backend-python/.env.example services/backend-python/.env
```

Edit `services/backend-python/.env` and fill in:

```
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
SECRET_KEY=any-long-random-string-used-to-sign-session-cookies
```

Leave all other values as they are for local development.

Generate a good SECRET_KEY with:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 4 — Run the backend

```bash
cd services/backend-python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Backend runs at `http://localhost:8080`.

FastAPI generates interactive API docs automatically at `http://localhost:8080/docs`.

---

## Step 5 — Run the frontend

In a separate terminal:

```bash
cd apps/frontend && npm install && npm run dev
```

Frontend runs at `http://localhost:3000`.

---

## Useful URLs

| URL | What it does |
|---|---|
| http://localhost:3000 | Landing page |
| http://localhost:3000/dashboard | Dashboard (requires login) |
| http://localhost:8080/auth/google | Starts Google login |
| http://localhost:8080/api/v1/me | Returns current user JSON |
| http://localhost:8080/health | Backend health |
| http://localhost:8080/logout | Logs out |
| http://localhost:8080/docs | FastAPI OpenAPI docs |

---

## Inspect the database manually

```bash
docker exec -it memoryos-postgres psql -U memoryos -d memoryos
```

Useful commands inside psql:

```sql
\dt                                    -- list all tables
\d app_user                            -- describe a table
SELECT * FROM app_user;               -- see all users
SELECT * FROM flyway_schema_history;  -- see which migrations ran
\q                                     -- quit
```

Or connect with a GUI (TablePlus, DBeaver, pgAdmin):
- Host: `localhost`, Port: `5432`, DB: `memoryos`, User: `memoryos`, Password: `memoryos`

---

## Run backend tests

```bash
cd services/backend-python
source .venv/bin/activate
ENV_FILE=.env.test python -m pytest tests/ -v
```

Tests use SQLite in-memory. No real PostgreSQL or Google credentials needed.

## Run frontend checks

```bash
cd apps/frontend && npm run typecheck && npm run build
```
