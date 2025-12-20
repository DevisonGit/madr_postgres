from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from madr_postgres.models.users import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def read(self, user: User) -> User:
        return await self.session.scalar(
            select(User).where(
                (User.username == user.username) | (User.email == user.email)
            )
        )

    async def delete(self, user_id: int):
        await self.session.delete(user_id)
        return await self.session.commit()

    async def read_by_id(self, user_id: int):
        return await self.session.get(User, user_id)

    async def patch(self, user: User):
        return await self.create(user)
