# Local Development

## Prerequisites

- Java 21 for backend development.
- Maven 3.9+.
- Node.js 22+.
- npm 11+.
- PostgreSQL 15+.
- Google OAuth client credentials.

## Backend

Path:

```text
services/backend
```

Environment variables are documented in:

```text
services/backend/.env.example
```

Start PostgreSQL:

```bash
docker compose -f infra/docker/docker-compose.local.yml up -d
```

Run tests:

```bash
mvn test
```

Run locally:

```bash
mvn spring-boot:run
```

The backend starts on `http://localhost:8080`.

## Frontend

Path:

```text
apps/frontend
```

Environment variables are documented in:

```text
apps/frontend/.env.example
```

Install dependencies:

```bash
npm install
```

Run locally:

```bash
npm run dev
```

The frontend starts on `http://localhost:3000`.

## Google OAuth Redirect

For local development, configure the Google OAuth redirect URI as:

```text
http://localhost:8080/login/oauth2/code/google
```
