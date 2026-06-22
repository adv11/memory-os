# Backend

Target stack:

- Spring Boot 3.x
- Java 21
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

Copy `.env.example` into your shell or local environment manager, then run:

```bash
mvn spring-boot:run
```

The backend requires Java 21 for the production target.

See `/docs/project/local-development.md` for setup details.
