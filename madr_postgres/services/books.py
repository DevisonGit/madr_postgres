from ..models import Book
from ..repositories.books import BookRepository
from ..schemas.books import BookCreate, BookUpdate, FilterBook
from ..utils.sanitize import sanitize_string


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def create_book(self, data: BookCreate):
        book = Book(**data.model_dump())
        book.title = sanitize_string(book.title)
        return await self.repo.create(book)

    async def delete(self, book_id: int):
        book = await self.repo.get_by_id(book_id)
        await self.repo.delete(book)
        return {'message': 'Book deleted in MADR'}

    async def patch_book(self, book_id: int, data: BookUpdate):
        book = await self.repo.get_by_id(book_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        book.title = sanitize_string(book.title)

        return await self.repo.patch(book)

    async def read_by_id(self, user_id: int):
        return await self.repo.get_by_id(user_id)

    async def read_book(self, book_filter: FilterBook):
        books = await self.repo.read_filter(book_filter)
        return {'books': books.all()}
