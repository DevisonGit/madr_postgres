from http import HTTPStatus


def test_patch_book(client, book, author, token):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test', 'year': 2012},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'test',
        'year': 2012,
        'author_id': author.id,
    }


def test_patch_book_integrity_error(client, book, other_book, token):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': other_book.title, 'year': 2012},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book already exists in MADR'}


def test_patch_book_not_found(client, book, token):
    response = client.patch(
        f'/books/{book.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test', 'year': 2012},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}
