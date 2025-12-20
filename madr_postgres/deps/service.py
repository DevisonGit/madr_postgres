from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from madr_postgres.db.database import get_session
from madr_postgres.repositories import auth as auth_repo
from madr_postgres.repositories import users as users_repo
from madr_postgres.services import auth, users

Session = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: Session):
    repo = users_repo.UserRepository(session)
    return users.UserService(repo)


def get_auth_service(session: Session):
    repo = auth_repo.AuthRepository(session)
    return auth.AuthService(repo)
