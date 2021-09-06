"""
The url shortener backend.
"""

from fastapi import FastAPI
from backend.routes import router

def build_app(app: FastAPI) -> FastAPI:
    app.include_router(router)
    return app

app = build_app(FastAPI())