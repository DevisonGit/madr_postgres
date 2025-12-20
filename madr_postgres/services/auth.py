from fastapi.security import OAuth2PasswordRequestForm

from ..core.security import create_access_token, verify_password
from ..exceptions.auth import AuthUnauthorized
from ..models import User
from ..repositories.auth import AuthRepository


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    async def access_token(self, form_data: OAuth2PasswordRequestForm):
        user = await self.repo.read(form_data.username)

        if not user:
            raise AuthUnauthorized()

        if not verify_password(form_data.password, user.password):
            raise AuthUnauthorized()

        access_token = create_access_token(data={'sub': user.email})

        return {'access_token': access_token, 'token_type': 'bearer'}

    @staticmethod
    async def refresh_access_token(user: User):
        new_access_token = create_access_token(data={'sub': user.email})

        return {'access_token': new_access_token, 'token_type': 'bearer'}

    async def validate_current_user(self, email: str):
        return await self.repo.read(email)
