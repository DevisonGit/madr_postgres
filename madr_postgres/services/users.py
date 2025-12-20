from sqlalchemy.exc import IntegrityError

from madr_postgres.exceptions.users import UserAlreadyExists, UserNotFound
from madr_postgres.models.users import User
from madr_postgres.repositories.users import UserRepository
from madr_postgres.schemas.users import UserCreate, UserUpdate
from madr_postgres.utils.sanitize import sanitize_string


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate):
        user = User(**data.model_dump())
        user.username = sanitize_string(user.username)

        user_db = await self.repo.read(user)

        if user_db:
            if user_db.username == user.username:
                raise UserAlreadyExists('Username')
            if user_db.email == user.email:
                raise UserAlreadyExists('Email')

        return await self.repo.create(user)

    async def delete_user(self, user_id: int):
        user = await self.repo.read_by_id(user_id)
        if not user:
            raise UserNotFound()
        await self.repo.delete(user)
        return {'message': 'User deleted'}

    async def patch_user(self, user_id: int, user: UserUpdate):
        db_user = await self.repo.read_by_id(user_id)

        if not db_user:
            raise UserNotFound()

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db_user.username = sanitize_string(db_user.username)

        try:
            return await self.repo.patch(db_user)
        except IntegrityError:
            raise UserAlreadyExists('Username or email')
