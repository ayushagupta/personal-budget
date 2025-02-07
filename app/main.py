from fastapi import FastAPI
from app.routers import categories, auth, users

app = FastAPI(
    title="Personal Budget App"
)

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(auth.router)