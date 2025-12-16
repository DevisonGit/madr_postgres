from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from madr_postgres.db.base import table_registry


@table_registry.mapped
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[int]
    title: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), server_onupdate=func.now()
    )
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
