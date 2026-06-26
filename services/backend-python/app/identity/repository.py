import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.identity.model import AppUser


async def find_by_google_id(db: AsyncSession, google_id: str) -> Optional[AppUser]:
    result = await db.execute(select(AppUser).where(AppUser.google_id == google_id))
    return result.scalar_one_or_none()


async def find_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[AppUser]:
    result = await db.execute(select(AppUser).where(AppUser.id == user_id))
    return result.scalar_one_or_none()


async def upsert_from_google(db: AsyncSession, google_id: str, email: str, name: str) -> AppUser:
    """Create user on first login, update email and name on subsequent logins."""
    user = await find_by_google_id(db, google_id)
    if user:
        user.email = email
        user.name = name
    else:
        user = AppUser(id=uuid.uuid4(), google_id=google_id, email=email, name=name)
        db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
