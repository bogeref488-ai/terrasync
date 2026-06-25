from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/")
def list_reports():
    return [
        {
            "report_no": "RPT-2026-0001",
            "work_order_no": "WO-2026-0001",
            "site_id": "KMP-001",
            "report_type": "Tower Inspection Report",
            "status": "Draft",
        }
    ]


@router.post("/")
def create_report(payload: dict):
    return {
        "message": "Report creation endpoint ready",
        "data": payload,
    }
