from datetime import datetime, timezone

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ApiErrorResponse(BaseModel):
    code: str
    message: str
    details: list[str] = []
    timestamp: str


def _error(code: str, message: str, details: list[str] = []) -> dict:
    return ApiErrorResponse(
        code=code,
        message=message,
        details=details,
        timestamp=datetime.now(timezone.utc).isoformat(),
    ).model_dump()


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [f"{'.'.join(str(l) for l in e['loc'])}: {e['msg']}" for e in exc.errors()]
    return JSONResponse(status_code=422, content=_error("VALIDATION_ERROR", "Request validation failed", details))


async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content=_error("NOT_FOUND", str(exc)))


async def conflict_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=409, content=_error("CONFLICT", str(exc)))


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=_error("INTERNAL_ERROR", "An unexpected error occurred"))
