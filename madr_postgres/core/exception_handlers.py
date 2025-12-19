from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from madr_postgres.exceptions.users import UserAlreadyExists, UserNotFound


def register_exception_handlers(app):
    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(_: Request, exc: UserNotFound):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'detail': 'User not found'},
        )

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_handler(_: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'detail': f'{exc} already exists'},
        )
