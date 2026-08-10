from pydantic import BaseModel


class SiteBase(BaseModel):
    site_id: str
    name: str
    country: str
    region: str
    district: str
    latitude: float
    longitude: float
    site_type: str
    status: str


class SiteCreate(SiteBase):
    pass


class SiteRead(SiteBase):
    id: int

    class Config:
        from_attributes = True