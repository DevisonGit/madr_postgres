from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from madr_postgres.deps import BookServiceDep, CurrentUser
from madr_postgres.schemas.books import (
    BookCreate,
    BookList,
    BookPublic,
    BookUpdate,
    FilterBook,
)
from madr_postgres.schemas.message import Message

router = APIRouter(prefix='/books', tags=['tags'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(
    data: BookCreate, service: BookServiceDep, user: CurrentUser
):
    return await service.create_book(data)


@router.get('/{book_id}', response_model=BookPublic)
async def read_by_id(book_id: int, service: BookServiceDep):
    return await service.read_by_id(book_id)


@router.patch('/{book_id}', response_model=BookPublic)
async def patch_book(
    book_id: int, data: BookUpdate, service: BookServiceDep, user: CurrentUser
):
    return await service.patch_book(book_id, data)


@router.delete('/{book_id}', response_model=Message)
async def delete_book(
    book_id: int, user: CurrentUser, service: BookServiceDep
):
    return await service.delete(book_id)


@router.get('/', response_model=BookList)
async def read_books(
    service: BookServiceDep, filter_book: Annotated[FilterBook, Query()]
):
    return await service.read_book(filter_book)
