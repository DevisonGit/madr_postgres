import pytest_asyncio

from madr_postgres.core.security import get_password_hash

from .factory import UserFactory


@pytest_asyncio.fixture
async def user(session):
    password = 'test@secret'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'test@secret'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
