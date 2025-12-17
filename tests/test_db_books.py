from dataclasses import asdict

import pytest
from sqlalchemy import select

from madr_postgres.models.books import Book


@pytest.mark.asyncio
async def test_create_book(author, session, mock_db_time):
    with mock_db_time(model=Book) as time:
        new_book = Book(title='test', year=2012, author_id=author.id)
        session.add(new_book)
        await session.commit()

        book = await session.scalar(select(Book).where(Book.title == 'test'))

        assert asdict(book) == {
            'id': 1,
            'title': 'test',
            'year': 2012,
            'created_at': time,
            'updated_at': time,
            'author_id': author.id,
        }
