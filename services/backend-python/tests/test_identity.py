from __future__ import annotations

import uuid

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.identity import repository
from app.identity.model import AppUser


class TestUpsertFromGoogle:
    async def test_creates_user_on_first_login(self, db: AsyncSession):
        user = await repository.upsert_from_google(
            db, google_id="google-123", email="ava@example.com", name="Ava"
        )

        assert user.id is not None
        assert user.google_id == "google-123"
        assert user.email == "ava@example.com"
        assert user.name == "Ava"
        assert user.created_at is not None
        assert user.updated_at is not None

        found = await repository.find_by_google_id(db, "google-123")
        assert found is not None
        assert found.id == user.id

    async def test_updates_profile_on_subsequent_login(self, db: AsyncSession):
        await repository.upsert_from_google(
            db, google_id="google-123", email="old@example.com", name="Old Name"
        )

        updated = await repository.upsert_from_google(
            db, google_id="google-123", email="new@example.com", name="New Name"
        )

        assert updated.email == "new@example.com"
        assert updated.name == "New Name"

        count = await db.execute(select(func.count()).select_from(AppUser))
        assert count.scalar() == 1

    async def test_find_by_id_returns_none_for_unknown(self, db: AsyncSession):
        result = await repository.find_by_id(db, uuid.uuid4())
        assert result is None

    async def test_find_by_google_id_returns_none_for_unknown(self, db: AsyncSession):
        result = await repository.find_by_google_id(db, "nonexistent")
        assert result is None

    async def test_two_different_users_are_separate_rows(self, db: AsyncSession):
        await repository.upsert_from_google(db, "g-1", "alice@example.com", "Alice")
        await repository.upsert_from_google(db, "g-2", "bob@example.com", "Bob")

        count = await db.execute(select(func.count()).select_from(AppUser))
        assert count.scalar() == 2


class TestIdentityIntegration:
    async def test_create_then_find_by_id(self, db: AsyncSession):
        user = await repository.upsert_from_google(
            db, google_id="g-integration", email="int@example.com", name="Integration"
        )
        found = await repository.find_by_id(db, user.id)

        assert found is not None
        assert found.email == "int@example.com"
        assert found.google_id == "g-integration"

    async def test_upsert_is_idempotent(self, db: AsyncSession):
        for name in ["First", "Second", "Third"]:
            await repository.upsert_from_google(db, "g-idem", "x@example.com", name)

        count = await db.execute(select(func.count()).select_from(AppUser))
        assert count.scalar() == 1

        final = await repository.find_by_google_id(db, "g-idem")
        assert final.name == "Third"
