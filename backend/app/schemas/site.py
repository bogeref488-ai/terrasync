from pydantic import BaseModel


class SiteBase(BaseModel):
    site_id: str
    name: str
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class SiteCreate(SiteBase):
    pass


class SiteRead(SiteBase):
    id: int

    class Config:
        from_attributes = True
