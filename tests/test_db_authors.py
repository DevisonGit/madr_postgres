from dataclasses import asdict

import pytest
from sqlalchemy import select

from madr_postgres.models.authors import Author


@pytest.mark.asyncio
async def test_create_author(session, mock_db_time):
    with mock_db_time(model=Author) as time:
        new_author = Author(
            name='test',
        )
        session.add(new_author)
        await session.commit()

        author = await session.scalar(
            select(Author).where(Author.name == 'test')
        )

        assert asdict(author) == {
            'id': 1,
            'name': 'test',
            'created_at': time,
            'updated_at': time,
            'books': [],
        }
