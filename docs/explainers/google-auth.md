# Google Authentication

## What is this?

This is how users log in to MemoryOS. There are no passwords. Users click "Sign in with Google", get redirected to Google's consent screen, and come back logged in. On their first login, a user record is created in our database. On every login after that, their profile (name and email) is updated if it changed.

---

## Why was it built this way?

We chose Google OAuth for a few reasons:
- No password management. No forgot-password flows, no hashing, no breach risk from a password database.
- Users already trust Google with their identity.
- It connects naturally with Google Drive, which is planned for file storage in Phase 4.
- Spring Boot has first-class support for OAuth2 Login, so very little custom code is needed.

We use Spring Security's built-in OAuth2 Login rather than implementing the OAuth flow ourselves. Spring handles the redirect, the token exchange, and the user profile fetch. We only hook in at the end to save the user to our database.

---

## How does it work end to end?

### Step 1: User clicks login

The frontend has a login button that links to:
```
http://localhost:8080/login/oauth2/authorization/google
```
This is a Spring Security built-in URL. When hit, Spring redirects the user to Google's OAuth consent screen.

File: `apps/frontend/src/features/auth/LoginButton.tsx`

### Step 2: User consents on Google

Google shows the user a consent screen asking for permission to share their name, email, and profile. The user clicks "Allow".

### Step 3: Google redirects back to the backend

Google calls our backend at:
```
http://localhost:8080/login/oauth2/code/google
```
This redirect URI must be registered in Google Cloud Console. Spring Security handles this endpoint automatically.

### Step 4: Spring fetches the user profile

Spring exchanges the authorization code for tokens and then calls Google's userinfo endpoint to get the user's `sub` (Google ID), `email`, and `name`.

### Step 5: Our code runs — user provisioning

After Spring completes the OAuth handshake, it calls our custom success handler. This is wired in `SecurityConfig`:

```java
.oauth2Login(oauth -> oauth
    .successHandler((request, response, authentication) -> {
        provisioningService.provision(authentication);
        response.sendRedirect(webProperties.getSuccessUrl());
    })
)
```

File: `services/backend/src/main/java/com/memoryos/common/security/SecurityConfig.java`

The `provision` method in `OAuthUserProvisioningService`:
1. Extracts `sub`, `email`, and `name` from the Google profile.
2. Looks up the user by `google_id` in the database.
3. If found: updates `email` and `name` (they may have changed on Google).
4. If not found: creates a new `AppUser` with a fresh UUID.
5. Saves and returns the user.

File: `services/backend/src/main/java/com/memoryos/identity/service/OAuthUserProvisioningService.java`

### Step 6: Session is created

Spring Security creates a server-side session and sends a session cookie (`JSESSIONID`) to the browser. All future requests from this browser carry that cookie and are considered authenticated.

### Step 7: User lands on the dashboard

The success handler redirects to `http://localhost:3000/dashboard` (configurable via `MEMORYOS_WEB_SUCCESS_URL`).

### Step 8: Frontend fetches the current user

The dashboard calls `GET /api/v1/me` to get the logged-in user's details.

File: `services/backend/src/main/java/com/memoryos/identity/controller/MeController.java`

The `MeController` calls `AuthenticatedUserService.requireCurrentUser()` which:
1. Reads the `Authentication` object from the current Spring Security context.
2. Extracts the Google `sub` (Google ID) from the OAuth2 principal.
3. Looks up the `AppUser` in the database by that Google ID.
4. Returns it, or throws if somehow the user is authenticated but not in the database.

File: `services/backend/src/main/java/com/memoryos/identity/service/AuthenticatedUserService.java`

---

## Database

One table is involved:

```sql
app_user (
  id           UUID PRIMARY KEY,        -- our internal ID, not Google's
  google_id    VARCHAR(128) UNIQUE,      -- Google's "sub" claim, stable forever
  email        VARCHAR(320) UNIQUE,      -- can change, updated on every login
  name         VARCHAR(200),             -- can change, updated on every login
  created_at   TIMESTAMPTZ,
  updated_at   TIMESTAMPTZ
)
```

Why `google_id` as the lookup key instead of email?
- Email can change. Google's `sub` claim is a permanent, stable identifier for a Google account. We use that to find returning users, then update their email if it changed.

Migration file: `services/backend/src/main/resources/db/migration/V1__create_identity.sql`

---

## API

### GET /api/v1/me

Returns the authenticated user's profile. Requires a valid session cookie.

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "Akash"
}
```

Returns `401 Unauthorized` if not logged in.

### POST /logout

Clears the session and redirects to `http://localhost:3000` (configurable via `MEMORYOS_WEB_LOGOUT_SUCCESS_URL`). Invalidates the `JSESSIONID` cookie.

---

## Configuration

All values are in `services/backend/.env` (copy from `.env.example`):

| Variable | What it is |
|---|---|
| `GOOGLE_CLIENT_ID` | From Google Cloud Console OAuth credentials |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console OAuth credentials |
| `MEMORYOS_WEB_SUCCESS_URL` | Where to redirect after login (default: `http://localhost:3000/dashboard`) |
| `MEMORYOS_WEB_LOGOUT_SUCCESS_URL` | Where to redirect after logout (default: `http://localhost:3000`) |

These map to `application.yml`:
```yaml
spring.security.oauth2.client.registration.google.client-id: ${GOOGLE_CLIENT_ID}
spring.security.oauth2.client.registration.google.client-secret: ${GOOGLE_CLIENT_SECRET}
```

---

## Tests

Two tests in `OAuthUserProvisioningServiceTest`:

1. `createsUserFromGoogleProfile` — first-time login creates a user in the database.
2. `updatesExistingUserProfile` — second login with changed email/name updates the record and does not create a duplicate.

Tests use `@DataJpaTest` with H2 in-memory database. No real Google call is made — the test constructs a fake `OAuth2User` principal directly.

File: `services/backend/src/test/java/com/memoryos/identity/service/OAuthUserProvisioningServiceTest.java`

Run them with:
```bash
cd services/backend && mvn test
```

---

## What to watch out for

**The `.env` file must be loaded before running.** Spring Boot does not automatically load `.env` files. Use:
```bash
export $(cat .env | xargs) && mvn spring-boot:run
```

**The redirect URI must match exactly.** If the URI registered in Google Cloud Console does not match what Spring sends, Google will reject the login with a `redirect_uri_mismatch` error. The correct URI for local dev is:
```
http://localhost:8080/login/oauth2/code/google
```

**CORS is configured for the frontend origin.** The `MEMORYOS_CORS_ALLOWED_ORIGINS` variable must include the frontend URL (`http://localhost:3000` locally). Session cookies require `allowCredentials: true`, which is already set.

**Cookies are not secure in local dev.** `MEMORYOS_COOKIE_SECURE=false` is correct for `http://localhost`. Set it to `true` in production (which runs over HTTPS).

**The `JSESSIONID` cookie is `HttpOnly`.** The frontend cannot read it via JavaScript, which is intentional. It is sent automatically with every request by the browser.
