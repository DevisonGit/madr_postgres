from http import HTTPStatus


def test_patch_author(client, author, token):
    expected_name = 'Test Name'
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': expected_name},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': expected_name.lower()}


def test_patch_author_integrity_error(client, author, other_author, token):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': other_author.name},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author already exists in MADR'}


def test_patch_author_not_found(client, author, token):
    response = client.patch(
        f'/authors/{author.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'test'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}
