from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from madr_postgres.models.users import User


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read(self, email: str) -> User:
        return await self.session.scalar(
            select(User).where(User.email == email)
        )
