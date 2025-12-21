from http import HTTPStatus


def test_patch_user(client, user, token):
    expected_username = 'test'
    response = client.patch(
        f'/users/{user.id}',
        json={'username': expected_username},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == expected_username


def test_patch_user_not_found(client, other_user, token):
    response = client.patch(
        f'/users/{other_user.id}',
        json={'username': 'test'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions'}


def test_patch_user_integrity_error(client, user, other_user, token):
    response = client.patch(
        f'/users/{user.id}',
        json={'username': other_user.username},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_patch_user_with_password(client, user, token):
    expected_username = 'test'
    response = client.patch(
        f'/users/{user.id}',
        json={'username': expected_username, 'password': 'test'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == expected_username
