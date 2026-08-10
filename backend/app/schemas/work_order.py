from pydantic import BaseModel


class WorkOrderBase(BaseModel):
    work_order_id: str
    site_id: str
    title: str
    description: str
    priority: str
    status: str
    assigned_to: str


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderRead(WorkOrderBase):
    id: int

    class Config:
        from_attributes = True
