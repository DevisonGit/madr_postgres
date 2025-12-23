from fastapi import FastAPI

from madr_postgres.core.exception_handlers import register_exception_handlers
from madr_postgres.routers import auth, authors, books, health, users

app = FastAPI()

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)
