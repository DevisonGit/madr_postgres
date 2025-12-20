from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from madr_postgres.deps.service import get_user_service
from madr_postgres.schemas.message import Message
from madr_postgres.schemas.users import UserCreate, UserPublic, UserUpdate
from madr_postgres.services.users import UserService

router = APIRouter(prefix='/users', tags=['users'])

Service = Annotated[UserService, Depends(get_user_service)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(data: UserCreate, service: Service):
    return await service.create_user(data)


@router.patch('/{user_id}', response_model=UserPublic)
async def patch_user(user_id: int, data: UserUpdate, service: Service):
    return await service.patch_user(user_id, data)


@router.delete('/{user_id}', response_model=Message)
async def delete_user(user_id: int, service: Service):
    return await service.delete_user(user_id)
