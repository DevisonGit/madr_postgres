from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from madr_postgres.exceptions.base import AlreadyExists, NotFound
from madr_postgres.models import Author
from madr_postgres.schemas.authors import FilterAuthor


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.resource_name = 'Author'

    async def create(self, author: Author) -> Author:
        try:
            self.session.add(author)
            await self.session.commit()
            await self.session.refresh(author)
            return author
        except IntegrityError:
            raise AlreadyExists(self.resource_name)

    async def delete(self, author: Author) -> None:
        await self.session.delete(author)
        return await self.session.commit()

    async def patch(self, author: Author):
        return await self.create(author)

    async def get_by_id(self, author_id: int) -> Author:
        author = await self.session.get(Author, author_id)
        if not author:
            raise NotFound(self.resource_name)
        return author

    async def read_filter(self, author_filter: FilterAuthor):
        query = select(Author)
        if author_filter.name:
            query = query.filter(Author.name.contains(author_filter.name))
        return await self.session.scalars(
            query.offset(author_filter.offset).limit(author_filter.limit)
        )
