from fastapi import FastAPI

from madr_postgres.routers import health

app = FastAPI()


app.include_router(health.router)
