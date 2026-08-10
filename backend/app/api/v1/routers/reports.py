from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.report import Report
from app.models.site import Site
from app.models.work_order import WorkOrder
from app.schemas.report import ReportCreate, ReportRead


router = APIRouter()


@router.get("/", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).order_by(Report.id.desc()).all()
    return reports


@router.post(
    "/",
    response_model=ReportRead,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
):
    site = (
        db.query(Site)
        .filter(Site.site_id == report_in.site_id)
        .first()
    )

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found. Create the site before creating a report.",
        )

    work_order = (
        db.query(WorkOrder)
        .filter(WorkOrder.work_order_id == report_in.work_order_id)
        .first()
    )

    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order not found. Create the work order before creating a report.",
        )

    if work_order.site_id != report_in.site_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work order does not belong to the provided site.",
        )

    existing_report = (
        db.query(Report)
        .filter(Report.report_id == report_in.report_id)
        .first()
    )

    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report ID already exists.",
        )

    report = Report(
        report_id=report_in.report_id,
        work_order_id=report_in.work_order_id,
        site_id=report_in.site_id,
        inspector_name=report_in.inspector_name,
        inspection_status=report_in.inspection_status,
        findings=report_in.findings,
        recommendations=report_in.recommendations,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report