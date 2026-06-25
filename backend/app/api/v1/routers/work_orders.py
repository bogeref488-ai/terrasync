from fastapi import APIRouter

router = APIRouter(prefix="/work-orders", tags=["work orders"])


@router.get("/")
def list_work_orders():
    return [
        {
            "work_order_no": "WO-2026-0001",
            "site_id": "KMP-001",
            "report_type": "Tower Inspection Report",
            "priority": "High",
            "status": "Assigned",
            "assigned_to": "Field Engineer",
        }
    ]


@router.post("/")
def create_work_order(payload: dict):
    return {
        "message": "Work order creation endpoint ready",
        "data": payload,
    }
