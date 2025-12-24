from http import HTTPStatus

from madr_postgres.schemas.books import BookPublic


def test_read_book(client, book, token):
    book_shema = BookPublic.model_validate(book).model_dump()
    response = client.get(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == book_shema


def test_read_books_empty(client, token):
    response = client.get(
        '/books/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


def test_read_books_with_book(client, book, token):
    book_shema = BookPublic.model_validate(book).model_dump()
    response = client.get(
        '/books/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book_shema]}


def test_read_books_filter_title(client, book, token):
    book_shema = BookPublic.model_validate(book).model_dump()
    response = client.get(
        f'/books/?&title={book.title}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book_shema]}


def test_read_books_filter_year(client, book, token):
    book_shema = BookPublic.model_validate(book).model_dump()
    response = client.get(
        f'/books/?&year={book.year}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book_shema]}


def test_read_books_not_found(client, book, token):
    response = client.get(
        f'/books/{book.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}
