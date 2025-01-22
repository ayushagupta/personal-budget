from fastapi import FastAPI
from app.routers import categories

app = FastAPI(
    title="Personal Budget App"
)

app.include_router(categories.router)