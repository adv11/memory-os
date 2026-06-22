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

Then run the backend with a Java 25 JDK:

```bash
export JAVA_HOME=/path/to/your/jdk-25
mvn spring-boot:run
```

The backend requires Java 25 for the production target.

See [docs/project/local-development.md](../../docs/project/local-development.md) for the full local setup flow.
