from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from madr_postgres.deps import AuthServiceDep
from madr_postgres.schemas.auth import Token

from ..deps.aliases import CurrentUser

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2Form, service: AuthServiceDep
):
    return await service.access_token(form_data)


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser, service: AuthServiceDep):
    return await service.refresh_access_token(user)
