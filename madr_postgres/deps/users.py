from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode

from ..core.settings import Settings
from ..exceptions.auth import AuthCredentialValidate
from ..services.auth import AuthService
from .service import get_auth_service

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh'
)
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    service: AuthServiceDep, token: str = Depends(oauth2_scheme)
):
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise AuthCredentialValidate()
    except DecodeError:
        raise AuthCredentialValidate()
    except ExpiredSignatureError:
        raise AuthCredentialValidate()

    user = await service.validate_current_user(subject_email)

    if not user:
        raise AuthCredentialValidate()

    return user
