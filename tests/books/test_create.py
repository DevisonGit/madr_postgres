from http import HTTPStatus


def test_create_book(client, author, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test', 'year': 2012, 'author_id': author.id},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'test',
        'year': 2012,
        'author_id': author.id,
    }


def test_create_book_already_exists(client, author, book, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': book.title, 'year': 2020, 'author_id': author.id},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book already exists in MADR'}


def test_create_book_author_not_found(client, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test', 'year': 2020, 'author_id': 2},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}
