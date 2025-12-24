from http import HTTPStatus

from madr_postgres.schemas.authors import AuthorPublic


def test_read_author(client, author, token):
    author_schema = AuthorPublic.model_validate(author).model_dump()
    response = client.get(
        f'/authors/{author.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == author_schema


def test_read_authors_empty(client, token):
    response = client.get(
        '/authors/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': []}


def test_read_authors_with_author(client, author, token):
    author_schema = AuthorPublic.model_validate(author).model_dump()
    response = client.get(
        '/authors/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': [author_schema]}


def test_read_authors_filter(client, author, token):
    author_schema = AuthorPublic.model_validate(author).model_dump()
    response = client.get(
        f'/authors/?&name={author.name}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': [author_schema]}


def test_read_author_not_found(client, author, token):
    response = client.get(
        f'/authors/{author.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}
