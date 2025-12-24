from pydantic import BaseModel, ConfigDict, Field

from madr_postgres.schemas.filter import FilterPage


class AuthorCreate(BaseModel):
    name: str


class AuthorPublic(AuthorCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorList(BaseModel):
    authors: list[AuthorPublic]


class FilterAuthor(FilterPage):
    name: str | None = Field(None, max_length=20)
