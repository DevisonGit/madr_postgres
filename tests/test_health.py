from http import HTTPStatus


def test_health_check_ok(client):
    response = client.get('/health')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'ok'}
