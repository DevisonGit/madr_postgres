from http import HTTPStatus

from fastapi import APIRouter

from madr_postgres.deps import CurrentUser, UserServiceDep
from madr_postgres.schemas.message import Message
from madr_postgres.schemas.users import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(data: UserCreate, service: UserServiceDep):
    return await service.create_user(data)


@router.patch('/{user_id}', response_model=UserPublic)
async def patch_user(
    user_id: int, data: UserUpdate, service: UserServiceDep, user: CurrentUser
):
    return await service.patch_user(user_id, data, user)


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int, service: UserServiceDep, user: CurrentUser
):
    return await service.delete_user(user_id, user)
