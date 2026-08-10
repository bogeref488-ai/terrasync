from pydantic import BaseModel


class ReportBase(BaseModel):
    report_id: str
    work_order_id: str
    site_id: str
    inspector_name: str
    inspection_status: str
    findings: str
    recommendations: str


class ReportCreate(ReportBase):
    pass


class ReportRead(ReportBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True