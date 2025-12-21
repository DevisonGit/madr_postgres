from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from madr_postgres.exceptions.auth import (
    AuthCredentialValidate,
    AuthUnauthorized,
)
from madr_postgres.exceptions.base import AlreadyExists, NotFound
from madr_postgres.exceptions.users import (
    UserAlreadyExists,
    UserNotPermission,
)


def register_exception_handlers(app):
    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_handler(_: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'detail': f'{exc} already exists'},
        )

    @app.exception_handler(AuthUnauthorized)
    async def auth_unauthorized(_: Request, exc: AuthUnauthorized):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={'detail': 'Incorrect email or password'},
        )

    @app.exception_handler(AuthCredentialValidate)
    async def auth_credential_handler(_: Request, exc: AuthCredentialValidate):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={'detail': 'Could not validate credentials'},
        )

    @app.exception_handler(UserNotPermission)
    async def auth_not_permission_handler(_: Request, exc: UserNotPermission):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={'detail': 'Not enough permissions'},
        )

    @app.exception_handler(AlreadyExists)
    async def already_exists_handler(_: Request, exc: AlreadyExists):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'detail': f'{exc} already exists in MADR'},
        )

    @app.exception_handler(NotFound)
    async def not_found_handler(_: Request, exc: NotFound):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'detail': f'{exc} not found in MADR'},
        )
