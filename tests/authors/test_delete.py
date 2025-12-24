from http import HTTPStatus


def test_delete_author(client, author, token):
    response = client.delete(
        f'/authors/{author.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author deleted in MADR'}


def test_delete_author_not_found(client, author, token):
    response = client.delete(
        f'/authors/{author.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


def test_delete_author_user_not_authenticated(client, author):
    response = client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': 'Bearer invalid'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
