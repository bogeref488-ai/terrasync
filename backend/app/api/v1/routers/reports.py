import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.inspection_template import InspectionTemplate
from app.models.report import Report
from app.models.site import Site
from app.models.work_order import WorkOrder
from app.policies.report_rules import get_report_photo_rule
from app.schemas.report import (
    ReportApprovalUpdate,
    ReportCreate,
    ReportRead,

)

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
        "coordinator_name": report.coordinator_name,
        "coordinator_comment": report.coordinator_comment,
        "reviewed_at": report.reviewed_at,
        "findings": report.findings,
        "recommendations": report.recommendations,
        "answers": json.loads(report.answers),
        "defects": json.loads(report.defects) if report.defects else [],
        "created_at": report.created_at,
    }


def count_reports_by_field(db: Session, field):
    rows = (
        db.query(field, func.count(Report.id))
        .group_by(field)
        .all()
    )

    return [
        {
            "name": row[0] or "Unknown",
            "count": row[1],
        }
        for row in rows
    ]


def get_defects_by_severity(db: Session) -> list[dict]:
    reports = db.query(Report).all()

    severity_counts: dict[str, int] = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
        "Critical": 0,
        "Unknown": 0,
    }

    for report in reports:
        if not report.defects:
            continue

        try:
            defects = json.loads(report.defects)
        except json.JSONDecodeError:
            continue

        for defect in defects:
            severity = defect.get("severity") or "Unknown"

            if severity not in severity_counts:
                severity_counts[severity] = 0

            severity_counts[severity] += 1

    return [
        {
            "severity": severity,
            "count": count,
        }
        for severity, count in severity_counts.items()
    ]


@router.get("/dashboard/status", response_model=dict)
def report_status_dashboard(db: Session = Depends(get_db)):
    total_reports = db.query(Report).count()

    pending_review = (
        db.query(Report)
        .filter(Report.approval_status == "Pending Review")
        .count()
    )

    approved = (
        db.query(Report)
        .filter(Report.approval_status == "Approved")
        .count()
    )

    rejected = (
        db.query(Report)
        .filter(Report.approval_status == "Rejected")
        .count()
    )

    changes_requested = (
        db.query(Report)
        .filter(Report.approval_status == "Changes Requested")
        .count()
    )

    recent_reports = (
        db.query(Report)
        .order_by(Report.id.desc())
        .limit(5)
        .all()
    )

    return {
        "summary": {
            "total_reports": total_reports,
            "pending_review": pending_review,
            "approved": approved,
            "rejected": rejected,
            "changes_requested": changes_requested,
        },
        "reports_by_approval_status": count_reports_by_field(
            db,
            Report.approval_status,
        ),
        "reports_by_inspection_status": count_reports_by_field(
            db,
            Report.inspection_status,
        ),
        "reports_by_site": count_reports_by_field(
            db,
            Report.site_id,
        ),
        "reports_by_template": count_reports_by_field(
            db,
            Report.template_name,
        ),
        "defects_by_severity": get_defects_by_severity(db),
        "recent_reports": [
            {
                "report_id": report.report_id,
                "site_id": report.site_id,
                "template_name": report.template_name,
                "inspector_name": report.inspector_name,
                "approval_status": report.approval_status,
                "created_at": report.created_at,
            }
            for report in recent_reports
        ],
    }


@router.get("/dashboard/summary", response_model=dict)
def report_dashboard_summary(db: Session = Depends(get_db)):
    return {
        "total_reports": db.query(Report).count(),
        "pending_review": db.query(Report).filter(
            Report.approval_status == "Pending Review"
        ).count(),
        "approved": db.query(Report).filter(
            Report.approval_status == "Approved"
        ).count(),
        "rejected": db.query(Report).filter(
            Report.approval_status == "Rejected"
        ).count(),
        "changes_requested": db.query(Report).filter(
            Report.approval_status == "Changes Requested"
        ).count(),
    }


@router.get("/dashboard/by-site", response_model=dict)
def reports_by_site(db: Session = Depends(get_db)):
    return {
        "reports_by_site": count_reports_by_field(db, Report.site_id),
    }


@router.get("/dashboard/by-template", response_model=dict)
def reports_by_template(db: Session = Depends(get_db)):
    return {
        "reports_by_template": count_reports_by_field(db, Report.template_name),
    }


@router.get("/dashboard/defects-by-severity", response_model=dict)
def defects_by_severity(db: Session = Depends(get_db)):
    return {
        "defects_by_severity": get_defects_by_severity(db),
    }

@router.get("/rules/photo-evidence", response_model=dict)
def get_photo_evidence_rule():
    return get_report_photo_rule()

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


@router.get("/approval/changes-requested/list", response_model=list[ReportRead])
def list_changes_requested_reports(db: Session = Depends(get_db)):
    reports = (
        db.query(Report)
        .filter(Report.approval_status == "Changes Requested")
        .order_by(Report.id.desc())
        .all()
    )

    return [serialize_report(report) for report in reports]