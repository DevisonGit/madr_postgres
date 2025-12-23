from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from madr_postgres.exceptions.base import AlreadyExists, NotFound
from madr_postgres.models import Book
from madr_postgres.schemas.books import FilterBook


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.resource_name = 'Book'

    async def create(self, book: Book):
        try:
            self.session.add(book)
            await self.session.commit()
            await self.session.refresh(book)
            return book
        except IntegrityError:
            raise AlreadyExists(self.resource_name)

    async def delete(self, book: Book):
        await self.session.delete(book)
        return await self.session.commit()

    async def patch(self, book: Book):
        return await self.create(book)

    async def get_by_id(self, book_id: int) -> Book:
        book: Optional[Book] = await self.session.get(Book, book_id)
        if not book:
            raise NotFound(self.resource_name)
        return book

    async def read_filter(self, book_filter: FilterBook):
        query = select(Book)
        if book_filter.year:
            query = query.filter(Book.year == book_filter.year)
        if book_filter.title:
            query = query.filter(Book.title.contains(book_filter.title))
        return await self.session.scalars(
            query.offset(book_filter.offset).limit(book_filter.limit)
        )
