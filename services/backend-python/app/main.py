from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.common.config import settings
from app.common.errors import (
    conflict_handler,
    generic_exception_handler,
    not_found_handler,
    validation_exception_handler,
)
from app.identity.router import router as identity_router

app = FastAPI(title="MemoryOS API", version="0.1.0")

# --- Middleware ---

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    https_only=settings.cookie_secure,
    same_site="lax",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-Requested-With"],
    allow_credentials=True,
)

# --- Exception handlers ---

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(409, conflict_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# --- Routers ---

app.include_router(identity_router)

# --- Health ---

@app.get("/health")
async def health():
    return {"status": "UP"}
