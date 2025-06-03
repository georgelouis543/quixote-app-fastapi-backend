from fastapi.middleware.cors import CORSMiddleware

from app.config.allowed_headers import allowed_headers
from app.config.allowed_methods import allowed_methods
from app.config.allowed_origns import allowed_origins


def add_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers
    )
