import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.inspection_template import InspectionTemplate
from app.models.report import Report
from app.models.site import Site
from app.models.work_order import WorkOrder
from app.schemas.report import ReportApprovalUpdate, ReportCreate, ReportRead

router = APIRouter()


VALID_APPROVAL_STATUSES = [
    "Pending Review",
    "Approved",
    "Rejected",
    "Changes Requested",
]


def serialize_report(report: Report) -> dict:
    return {
        "id": report.id,
        "report_id": report.report_id,
        "work_order_id": report.work_order_id,
        "site_id": report.site_id,
        "template_id": report.template_id,
        "template_name": report.template_name,
        "inspector_name": report.inspector_name,
        "inspector_company": report.inspector_company,
        "inspection_status": report.inspection_status,
        "approval_status": report.approval_status,
        "findings": report.findings,
        "recommendations": report.recommendations,
        "answers": json.loads(report.answers),
        "defects": json.loads(report.defects) if report.defects else [],
        "created_at": report.created_at,
    }


@router.get("/", response_model=list[ReportRead])
def list_reports(
    approval_status: Optional[str] = Query(default=None),
    site_id: Optional[str] = Query(default=None),
    template_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Report)

    if approval_status:
        query = query.filter(Report.approval_status == approval_status)

    if site_id:
        query = query.filter(Report.site_id == site_id)

    if template_id:
        query = query.filter(Report.template_id == template_id)

    reports = query.order_by(Report.id.desc()).all()

    return [serialize_report(report) for report in reports]


@router.post("/", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_report(report_in: ReportCreate, db: Session = Depends(get_db)):
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

    site = db.query(Site).filter(Site.site_id == report_in.site_id).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found.",
        )

    work_order = (
        db.query(WorkOrder)
        .filter(WorkOrder.work_order_id == report_in.work_order_id)
        .first()
    )

    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order not found.",
        )

    if work_order.site_id != report_in.site_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work order does not belong to this site.",
        )

    template = (
        db.query(InspectionTemplate)
        .filter(InspectionTemplate.template_id == report_in.template_id)
        .filter(InspectionTemplate.status == "Active")
        .first()
    )

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active inspection template not found.",
        )

    now = datetime.now(timezone.utc)

    report = Report(
        report_id=report_in.report_id,
        work_order_id=report_in.work_order_id,
        site_id=report_in.site_id,
        template_id=report_in.template_id,
        template_name=template.name,
        inspector_name=report_in.inspector_name,
        inspector_company=report_in.inspector_company,
        inspection_status=report_in.inspection_status,
        approval_status="Pending Review",
        findings=report_in.findings,
        recommendations=report_in.recommendations,
        answers=json.dumps([answer.model_dump() for answer in report_in.answers]),
        defects=json.dumps([defect.model_dump() for defect in report_in.defects]),
        created_at=now.isoformat(),
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return serialize_report(report)


@router.get("/{report_id}", response_model=ReportRead)
def get_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return serialize_report(report)


@router.patch("/{report_id}/approval", response_model=dict)
def update_report_approval(
    report_id: str,
    approval_in: ReportApprovalUpdate,
    db: Session = Depends(get_db),
):
    report = db.query(Report).filter(Report.report_id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    if approval_in.approval_status not in VALID_APPROVAL_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid approval status. Use one of: {VALID_APPROVAL_STATUSES}",
        )

    now = datetime.now(timezone.utc)

    report.approval_status = approval_in.approval_status
    report.coordinator_name = approval_in.coordinator_name
    report.coordinator_comment = approval_in.coordinator_comment
    report.reviewed_at = now.isoformat()

    db.commit()
    db.refresh(report)

    return {
        "message": "Report approval status updated successfully.",
        "report_id": report.report_id,
        "approval_status": report.approval_status,
        "coordinator_name": report.coordinator_name,
        "coordinator_comment": report.coordinator_comment,
        "reviewed_at": report.reviewed_at,
    }


@router.get("/approval/pending/list", response_model=list[ReportRead])
def list_pending_reports(db: Session = Depends(get_db)):
    reports = (
        db.query(Report)
        .filter(Report.approval_status == "Pending Review")
        .order_by(Report.id.desc())
        .all()
    )

    return [serialize_report(report) for report in reports]


@router.get("/approval/approved/list", response_model=list[ReportRead])
def list_approved_reports(db: Session = Depends(get_db)):
    reports = (
        db.query(Report)
        .filter(Report.approval_status == "Approved")
        .order_by(Report.id.desc())
        .all()
    )

    return [serialize_report(report) for report in reports]


@router.get("/approval/rejected/list", response_model=list[ReportRead])
def list_rejected_reports(db: Session = Depends(get_db)):
    reports = (
        db.query(Report)
        .filter(Report.approval_status == "Rejected")
        .order_by(Report.id.desc())
        .all()
    )

    return [serialize_report(report) for report in reports]