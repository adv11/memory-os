# Google Authentication

## What is this?

This is how users log in to MemoryOS. There are no passwords. Users click "Sign in with Google", get redirected to Google's consent screen, and come back logged in. On their first login, a user record is created in our database. On every login after that, their profile (name and email) is updated if it changed.

---

## Why was it built this way?

We chose Google OAuth for a few reasons:
- No password management. No forgot-password flows, no hashing, no breach risk from a password database.
- Users already trust Google with their identity.
- It connects naturally with Google Drive, which is planned for file storage in Phase 4.
- The backend is Python/FastAPI. We use Authlib, which has first-class support for OAuth2 with Starlette/FastAPI. Very little custom code is needed.

We use Starlette's `SessionMiddleware` to store the logged-in user's ID in a server-side encrypted cookie (`session`).

---

## How does it work end to end?

### Step 1: User clicks login

The frontend has a login button that links to:
```
http://localhost:8080/auth/google
```

File: `apps/frontend/src/features/auth/LoginButton.tsx`
URL configured in: `apps/frontend/src/lib/config.ts`

### Step 2: Backend redirects to Google

The `google_login` function in `router.py` uses Authlib to build a Google OAuth redirect URL and sends the user there.

File: `services/backend-python/app/identity/router.py`

### Step 3: User consents on Google

Google shows the consent screen asking for name, email, and profile access.

### Step 4: Google redirects back

Google calls:
```
http://localhost:8080/auth/google/callback
```

This URI must be registered in Google Cloud Console exactly as shown.

### Step 5: Backend exchanges code for tokens and fetches profile

The `google_callback` function in `router.py`:
1. Calls `oauth.google.authorize_access_token(request)` — exchanges the authorization code for tokens and returns the user's profile (`userinfo`).
2. Extracts `sub` (Google's permanent user ID), `email`, and `name`.
3. Calls `repository.upsert_from_google()` to create or update the user in PostgreSQL.
4. Stores `user.id` in the session: `request.session["user_id"] = str(user.id)`.
5. Redirects to `http://localhost:3000/dashboard`.

### Step 6: Session cookie is set

Starlette's `SessionMiddleware` signs and encrypts the session data using `SECRET_KEY` and stores it in a cookie named `session`. All future requests from this browser carry that cookie.

### Step 7: Frontend fetches current user

The dashboard calls `GET /api/v1/me`. The `me` function in `router.py` calls `require_current_user`, which:
1. Reads `user_id` from the session cookie.
2. Looks up the `AppUser` in the database by that ID.
3. Returns it, or raises 401 if not found.

---

## Database

One table:

```sql
app_user (
  id           UUID PRIMARY KEY,
  google_id    VARCHAR(128) UNIQUE NOT NULL,   -- Google's "sub", permanent
  email        VARCHAR(320) UNIQUE NOT NULL,   -- updated on every login
  name         VARCHAR(200) NOT NULL,          -- updated on every login
  created_at   TIMESTAMPTZ NOT NULL,
  updated_at   TIMESTAMPTZ NOT NULL
)
```

Why `google_id` as the lookup key? Email can change. Google's `sub` is permanent for a Google account.

Migration: `services/backend-python/migrations/` — the `app_user` table was created by the initial SQL migration `V1__create_identity.sql`.

SQLAlchemy model: `services/backend-python/app/identity/model.py`

All queries: `services/backend-python/app/identity/repository.py`

---

## API

### GET /auth/google
Starts Google login. Redirects to Google's consent screen. No body.

### GET /auth/google/callback
Google redirects here after consent. Not called directly by the frontend.

### GET /api/v1/me
Returns the authenticated user's profile. Requires a valid session cookie.

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "Akash"
}
```

Returns `401` if not logged in.

### GET /logout or POST /logout
Clears the session cookie and redirects to `http://localhost:3000`.

---

## Configuration

All values in `services/backend-python/.env`:

| Variable | What it is |
|---|---|
| `GOOGLE_CLIENT_ID` | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console |
| `SECRET_KEY` | Any long random string — signs the session cookie |
| `WEB_SUCCESS_URL` | Where to redirect after login (default: `http://localhost:3000/dashboard`) |
| `WEB_LOGOUT_SUCCESS_URL` | Where to redirect after logout (default: `http://localhost:3000`) |

Generate a secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Tests

File: `services/backend-python/tests/test_identity.py`

| Test | What it covers |
|---|---|
| `test_creates_user_on_first_login` | First login creates a user row |
| `test_updates_profile_on_subsequent_login` | Second login updates email/name, no duplicate row |
| `test_find_by_id_returns_none_for_unknown` | Unknown ID returns None |
| `test_find_by_google_id_returns_none_for_unknown` | Unknown google_id returns None |
| `test_two_different_users_are_separate_rows` | Two google_ids = two rows |
| `test_create_then_find_by_id` | Integration: create then fetch by ID |
| `test_upsert_is_idempotent` | Three upserts with same google_id = one row, last name wins |

Run:
```bash
cd services/backend-python && ENV_FILE=.env.test python -m pytest tests/ -v
```

Tests use SQLite in-memory. No real PostgreSQL or Google credentials needed.

---

## What to watch out for

**`SECRET_KEY` must be set.** If it is missing or weak, session cookies can be forged. Generate it with `secrets.token_hex(32)` and never commit it.

**The redirect URI must match exactly.** If the URI registered in Google Cloud Console does not match what the backend sends, Google rejects the login with `redirect_uri_mismatch`. For local dev it must be:
```
http://localhost:8080/auth/google/callback
```

**`COOKIE_SECURE=false` for local dev.** The session cookie's `secure` flag must be false over plain HTTP. Set it to `true` in production (HTTPS only).

**The session cookie is `HttpOnly` by default in Starlette.** The frontend cannot read it via JavaScript. It is sent automatically by the browser on every request to the backend.

**CORS must allow credentials.** The `CORSMiddleware` is configured with `allow_credentials=True`. Without this, the browser will not send the session cookie on cross-origin requests from `localhost:3000` to `localhost:8080`.
