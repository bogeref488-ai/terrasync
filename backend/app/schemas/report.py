from typing import Any, Optional

from pydantic import BaseModel


class ReportAnswer(BaseModel):
    section_id: str
    item_id: str
    field_key: str
    label: str
    value: Any
    comment: Optional[str] = None
    photos: list[str] = []


class ReportDefect(BaseModel):
    section_id: str
    item_id: str
    field_key: str
    defect_title: str
    defect_description: str
    severity: str
    recommended_action: Optional[str] = None
    photos: list[str] = []


class ReportBase(BaseModel):
    report_id: str
    work_order_id: str
    site_id: str

    template_id: str
    inspector_name: str
    inspector_company: Optional[str] = None

    inspection_status: str = "Completed"
    findings: Optional[str] = None
    recommendations: Optional[str] = None

    answers: list[ReportAnswer]
    defects: list[ReportDefect] = []


class ReportCreate(ReportBase):
    pass


class ReportRead(ReportBase):
    id: int
    template_name: str
    approval_status: str
    created_at: str

    class Config:
        from_attributes = True


class ReportApprovalUpdate(BaseModel):
    approval_status: str
    coordinator_name: str
    coordinator_comment: Optional[str] = None