from http import HTTPStatus


def test_delete_book(client, book, token):
    response = client.delete(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted in MADR'}


def test_delete_book_not_found(client, book, token):
    response = client.delete(
        f'/books/{book.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


def test_delete_book_user_not_authenticated(client, book):
    response = client.delete(
        f'/books/{book.id + 1}', headers={'Authorization': 'Bearer invalid}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
