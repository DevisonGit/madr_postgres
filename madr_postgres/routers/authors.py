from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from madr_postgres.deps.aliases import AuthorServiceDep
from madr_postgres.schemas.authors import (
    AuthorCreate,
    AuthorList,
    AuthorPublic,
    FilterAuthor,
)
from madr_postgres.schemas.message import Message

router = APIRouter(prefix='/authors', tags=['authors'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
async def create_author(data: AuthorCreate, service: AuthorServiceDep):
    return await service.create_author(data)


@router.get('/{author_id}', response_model=AuthorPublic)
async def read_by_id(author_id: int, service: AuthorServiceDep):
    return await service.read_by_id(author_id)


@router.patch('/{author_id}', response_model=AuthorPublic)
async def patch_author(
    author_id: int, data: AuthorCreate, service: AuthorServiceDep
):
    return await service.patch_author(author_id, data)


@router.delete('/{author_id}', response_model=Message)
async def delete_author(author_id: int, service: AuthorServiceDep):
    return await service.delete(author_id)


@router.get('/', response_model=AuthorList)
async def list_authors(
    service: AuthorServiceDep, author_filter: Annotated[FilterAuthor, Query()]
):
    return await service.read_authors(author_filter)
