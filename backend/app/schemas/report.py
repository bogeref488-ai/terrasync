from pydantic import BaseModel


class ReportBase(BaseModel):
    report_no: str
    work_order_no: str
    site_id: str
    report_type: str
    status: str = "Draft"
    summary: str | None = None


class ReportCreate(ReportBase):
    pass


class ReportRead(ReportBase):
    id: int

    class Config:
        from_attributes = True
