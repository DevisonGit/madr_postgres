import factory

from madr_postgres.models.books import Book


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f'test{n}')
    year = 1882
