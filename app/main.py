from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import init_db
from app.middleware.app_middleware import add_middlewares
from app.routers import newsletter_routes, auth_routes, admin_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

add_middlewares(app)

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(newsletter_routes.router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to Quixote App - Built by Lord Wilmore"
    }
