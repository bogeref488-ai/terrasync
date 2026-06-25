from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TerraSync API",
        "message": "Reliable Field Operations. Anywhere.",
    }
