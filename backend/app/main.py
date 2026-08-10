from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import test_database_connection


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Offline-first field operations API for TerraSync.",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Welcome to TerraSync API",
        "status": "running",
        "docs": "/docs",
    }


@app.get(f"{settings.API_V1_PREFIX}/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": "TerraSync API",
        "version": "0.1.0",
    }


@app.get(f"{settings.API_V1_PREFIX}/db-test", tags=["database"])
def db_test():
    is_connected = test_database_connection()

    return {
        "database_connected": is_connected,
        "database_url": settings.DATABASE_URL,
    }


app.include_router(api_router, prefix=settings.API_V1_PREFIX)