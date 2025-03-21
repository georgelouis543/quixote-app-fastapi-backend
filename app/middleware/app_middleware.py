from fastapi.middleware.cors import CORSMiddleware


def add_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
            "Set-Cookie",
        ],
    )
