from typing import Any, Optional

from pydantic import BaseModel


class ReportPhoto(BaseModel):
    photo_type: str
    file_url: str
    caption: Optional[str] = None
    captured_at: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str = "mobile_app_camera"


class ReportAnswer(BaseModel):
    section_id: str
    item_id: str
    field_key: str
    label: str
    value: Any
    comment: Optional[str] = None
    photos: list[ReportPhoto] = []


class ReportDefect(BaseModel):
    section_id: str
    item_id: str
    field_key: str
    defect_title: str
    defect_description: str
    severity: str
    recommended_action: Optional[str] = None
    photos: list[ReportPhoto] = []


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
    coordinator_name: Optional[str] = None
    coordinator_comment: Optional[str] = None
    reviewed_at: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class ReportApprovalUpdate(BaseModel):
    approval_status: str
    coordinator_name: str
    coordinator_comment: Optional[str] = None

