import pytest_asyncio

from .factory import UserFactory


@pytest_asyncio.fixture
async def user(session):
    user = UserFactory()

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def other_user(session):
    user = UserFactory()

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
