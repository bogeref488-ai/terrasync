from pydantic import BaseModel


class WorkOrderBase(BaseModel):
    work_order_no: str
    site_id: str
    report_type: str
    priority: str = "Medium"
    status: str = "New"
    assigned_to: str | None = None


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderRead(WorkOrderBase):
    id: int

    class Config:
        from_attributes = True
