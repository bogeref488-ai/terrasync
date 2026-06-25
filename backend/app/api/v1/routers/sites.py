from fastapi import APIRouter

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/")
def list_sites():
    return [
        {
            "site_id": "KMP-001",
            "name": "Kampala Main Site",
            "region": "Central",
            "latitude": 0.3476,
            "longitude": 32.5825,
        }
    ]


@router.post("/")
def create_site(payload: dict):
    return {
        "message": "Site creation endpoint ready",
        "data": payload,
    }
