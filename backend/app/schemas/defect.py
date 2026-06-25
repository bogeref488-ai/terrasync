from pydantic import BaseModel


class DefectBase(BaseModel):
    defect_no: str
    report_no: str
    site_id: str
    category: str
    severity: str
    description: str
    recommendation: str | None = None
    status: str = "Open"


class DefectCreate(DefectBase):
    pass


class DefectRead(DefectBase):
    id: int

    class Config:
        from_attributes = True
