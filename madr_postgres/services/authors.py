from ..models import Author
from ..repositories.authors import AuthorRepository
from ..schemas.authors import AuthorCreate, FilterAuthor
from ..utils.sanitize import sanitize_string


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def create_author(self, data: AuthorCreate):
        author = Author(**data.model_dump())
        author.name = sanitize_string(author.name)
        return await self.repo.create(author)

    async def delete(self, author_id: int):
        author = await self.repo.get_by_id(author_id)
        await self.repo.delete(author)
        return {'message': 'Author deleted in MADR'}

    async def patch_author(self, author_id: int, data: AuthorCreate):
        author = await self.repo.get_by_id(author_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(author, key, value)
        author.name = sanitize_string(author.name)

        return await self.repo.patch(author)

    async def read_by_id(self, user_id: int) -> Author:
        return await self.repo.get_by_id(user_id)

    async def read_authors(self, author_filter: FilterAuthor):
        authors = await self.repo.read_filter(author_filter)
        return {'authors': authors.all()}
