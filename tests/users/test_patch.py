from http import HTTPStatus


def test_patch_user(client, user):
    expected_username = 'test'
    response = client.patch(
        f'/users/{user.id}', json={'username': expected_username}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == expected_username


def test_patch_user_not_found(client, user):
    response = client.patch(
        f'/users/{user.id + 1}', json={'username': 'test'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_patch_user_integrity_error(client, user, other_user):
    response = client.patch(
        f'/users/{user.id}',
        json={'username': other_user.username}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}
