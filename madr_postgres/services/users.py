from sqlalchemy.exc import IntegrityError

from madr_postgres.exceptions.users import (
    UserAlreadyExists,
    UserNotPermission,
)
from madr_postgres.models.users import User
from madr_postgres.repositories.users import UserRepository
from madr_postgres.schemas.users import UserCreate, UserUpdate
from madr_postgres.utils.sanitize import sanitize_string

from ..core.security import get_password_hash


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate):
        user = User(**data.model_dump())
        user.username = sanitize_string(user.username)
        user.password = get_password_hash(user.password)

        user_db = await self.repo.read(user)

        if user_db:
            if user_db.username == user.username:
                raise UserAlreadyExists('Username')
            if user_db.email == user.email:
                raise UserAlreadyExists('Email')

        return await self.repo.create(user)

    async def delete_user(self, user_id: int, current_user: User):
        if current_user.id != user_id:
            raise UserNotPermission()
        await self.repo.delete(current_user)
        return {'message': 'User deleted'}

    async def patch_user(
        self, user_id: int, user: UserUpdate, current_user: User
    ):
        if current_user.id != user_id:
            raise UserNotPermission()

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(current_user, key, value)

        current_user.username = sanitize_string(current_user.username)
        if user.password:
            current_user.password = get_password_hash(user.password)

        try:
            return await self.repo.patch(current_user)
        except IntegrityError:
            raise UserAlreadyExists('Username or email')
