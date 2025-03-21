from fastapi import FastAPI

from app.middleware.app_middleware import add_middlewares
from app.routers import newsletter_routes

app = FastAPI()

add_middlewares(app)

app.include_router(newsletter_routes.router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to Quixote App - Built by Lord Wilmore"
    }
