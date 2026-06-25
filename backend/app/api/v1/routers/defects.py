from fastapi import APIRouter

router = APIRouter(prefix="/defects", tags=["defects"])


@router.get("/")
def list_defects():
    return [
        {
            "defect_no": "DEF-2026-0001",
            "report_no": "RPT-2026-0001",
            "site_id": "KMP-001",
            "category": "Tower Structure",
            "severity": "Major",
            "description": "Rusted bolts observed on tower leg.",
            "status": "Open",
        }
    ]


@router.post("/")
def create_defect(payload: dict):
    return {
        "message": "Defect creation endpoint ready",
        "data": payload,
    }
