from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Offline-first field operations API for TerraSync.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "name": "TerraSync API",
        "tagline": "Reliable Field Operations. Anywhere.",
        "docs": "/docs",
    }
