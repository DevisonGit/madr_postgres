from datetime import datetime

from books import Book
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from madr_postgres.db.base import table_registry


@table_registry.mapped
class Author:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), server_onupdate=func.now()
    )
    books: Mapped[list['Book']] = relationship(
        init=False, cascade='all, delete, delete-orphan', lazy='selectin'
    )
