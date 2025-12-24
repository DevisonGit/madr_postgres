import datetime

from pydantic import BaseModel, ConfigDict, Field

from madr_postgres.schemas.filter import FilterPage


class BookCreate(BaseModel):
    year: int
    title: str
    author_id: int


class BookPublic(BookCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    books: list[BookPublic]


class FilterBook(FilterPage):
    title: str | None = Field(None, max_length=20)
    year: int | None = Field(None, lt=datetime.datetime.now().year)


class BookUpdate(BaseModel):
    year: int | None = None
    title: str | None = None
    author_id: int | None = None
