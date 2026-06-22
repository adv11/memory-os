# Backend

Target stack:

- Spring Boot 3.x
- Java 25
- Spring Security
- OAuth2 Login
- JPA/Hibernate
- Flyway
- PostgreSQL

## Implemented

- Spring Boot application scaffold.
- Google OAuth login configuration.
- User provisioning from Google profile.
- Authenticated `/api/v1/me` endpoint.
- Flyway migration for `app_user`.
- Baseline API error response handling.
- Health endpoint through Spring Boot Actuator.

## Run

Copy the example env file and fill in your real credentials before starting the app:

```bash
cp .env.example .env
```

Then run the backend:

```bash
cd services/backend && export $(cat .env | xargs) && mvn spring-boot:run
```

See [docs/project/local-development.md](../../docs/project/local-development.md) for the full local setup flow.
