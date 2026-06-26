import uuid
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.config import settings
from app.db.session import get_db
from app.identity import repository
from app.identity.schemas import CurrentUserResponse

router = APIRouter()

# --- OAuth client setup ---

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# --- Session helpers ---

SESSION_USER_KEY = "user_id"


def _get_session_user_id(request: Request) -> Optional[uuid.UUID]:
    raw = request.session.get(SESSION_USER_KEY)
    return uuid.UUID(raw) if raw else None


async def require_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
):
    user_id = _get_session_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = await repository.find_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User session is invalid")
    return user


# --- Auth routes ---

@router.get("/auth/google")
async def google_login(request: Request):
    """Redirect the user to Google's consent screen."""
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback", name="google_callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Google redirects here after consent.
    Exchange code for tokens, fetch profile, upsert user, store user_id in session.
    """
    token = await oauth.google.authorize_access_token(request)
    profile = token.get("userinfo")
    if not profile:
        raise HTTPException(status_code=400, detail="Google did not return a user profile")

    google_id = profile.get("sub")
    email = profile.get("email")
    name = profile.get("name") or email

    if not google_id or not email:
        raise HTTPException(status_code=400, detail="Missing required Google profile fields")

    user = await repository.upsert_from_google(db, google_id=google_id, email=email, name=name)
    request.session[SESSION_USER_KEY] = str(user.id)
    return RedirectResponse(url=settings.web_success_url)


@router.post("/logout")
@router.get("/logout")
async def logout(request: Request):
    """Clear the session and redirect to the frontend."""
    request.session.clear()
    return RedirectResponse(url=settings.web_logout_success_url)


# --- Identity API ---

@router.get("/api/v1/me", response_model=CurrentUserResponse)
async def me(user=Depends(require_current_user)):
    """Return the authenticated user's profile."""
    return CurrentUserResponse.model_validate(user)
