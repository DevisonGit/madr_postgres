from fastapi import FastAPI

from madr_postgres.core.exception_handlers import register_exception_handlers
from madr_postgres.routers import health, users

app = FastAPI()

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(users.router)
