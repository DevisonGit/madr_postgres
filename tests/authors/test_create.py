from http import HTTPStatus


def test_create_author(client, token):
    response = client.post(
        '/authors',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test name Author'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test name author'}


def test_create_author_already_exists(client, token, author):
    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': author.name},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author already exists in MADR'}
