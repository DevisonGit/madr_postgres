# MADR

O objetivo do projeto é criarmos um gerenciador de livros e relacionar com seus autores. 
## 🚀 Começando

Comandos utilizados durante o desenvolvimento

```
poetry new --flat nome_projeto
cd nome_projeto
poetry env use version_python
poetry install
pipx run ignr -p python > .gitignore
poetry add 'fastapi[standard]'
poetry add --group dev pytest pytest-cov taskipy ruff testcontainers pytest-asyncio
poetry add pydantic-settings
poetry add sqlalchemy
poetry add alembic
poetry add "sqlalchemy[asyncio]"
poetry add "psycopg[binary]"
alembic init migrations
chmod +x entrypoint.sh 
alembic revision --autogenerate -m 'create tables'
alembic upgrade head
poetry add --group dev factory-boy
poetry add pyjwt
poetry add --group dev freezegun
poetry add "pwdlib[argon2]"
gh secret set -f .env
```

