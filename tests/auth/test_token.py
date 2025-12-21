from http import HTTPStatus

from freezegun import freeze_time

from madr_postgres.core.security import create_access_token

TIME_INITIAL = '2025-01-01 12:00:00'
TIME_FINAL = '2025-01-01 13:00:01'


def test_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_invalid(client):
    response = client.post(
        '/auth/token', data={'username': 'invalid', 'password': 'invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_invalid_password(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': 'invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    refresh_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in refresh_token
    assert 'token_type' in refresh_token


def test_token_expired_after_time(client, user):
    with freeze_time(TIME_INITIAL):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time(TIME_FINAL):
        response = client.patch(
            f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token_expired_after_time(client, user):
    with freeze_time(TIME_INITIAL):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time(TIME_FINAL):
        response = client.post(
            '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_not_subject_email(client, user):
    data = {'test': 'test'}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_decode_error(client, user):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': 'Bearer invalid'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_not_user(client, other_user):
    data = {'sub': 'invalid'}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
