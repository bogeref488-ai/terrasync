from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.site import Site
from app.models.work_order import WorkOrder
from app.schemas.work_order import WorkOrderCreate, WorkOrderRead


router = APIRouter()


@router.get("/", response_model=list[WorkOrderRead])
def list_work_orders(db: Session = Depends(get_db)):
    work_orders = db.query(WorkOrder).order_by(WorkOrder.id.desc()).all()
    return work_orders


@router.post(
    "/",
    response_model=WorkOrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_work_order(
    work_order_in: WorkOrderCreate,
    db: Session = Depends(get_db),
):
    site = (
        db.query(Site)
        .filter(Site.site_id == work_order_in.site_id)
        .first()
    )

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found. Create the site before creating a work order.",
        )

    existing_work_order = (
        db.query(WorkOrder)
        .filter(WorkOrder.work_order_id == work_order_in.work_order_id)
        .first()
    )

    if existing_work_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work order ID already exists.",
        )

    work_order = WorkOrder(
        work_order_id=work_order_in.work_order_id,
        site_id=work_order_in.site_id,
        title=work_order_in.title,
        description=work_order_in.description,
        priority=work_order_in.priority,
        status=work_order_in.status,
        assigned_to=work_order_in.assigned_to,
    )

    db.add(work_order)
    db.commit()
    db.refresh(work_order)

    return work_order

@router.post("/")
def create_work_order(payload: dict):
    return {
        "message": "Work order creation endpoint ready",
        "data": payload,
    }
