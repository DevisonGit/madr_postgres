from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from madr_postgres.db.database import get_session
from madr_postgres.repositories.users import UserRepository
from madr_postgres.services.users import UserService

Session = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: Session):
    repo = UserRepository(session)
    return UserService(repo)
