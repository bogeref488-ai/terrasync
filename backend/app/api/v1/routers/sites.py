from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteRead


router = APIRouter()


@router.get("/", response_model=list[SiteRead])
def list_sites(db: Session = Depends(get_db)):
    sites = db.query(Site).order_by(Site.id.desc()).all()
    return sites


@router.post(
    "/",
    response_model=SiteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_site(
    site_in: SiteCreate,
    db: Session = Depends(get_db),
):
    existing_site = (
        db.query(Site)
        .filter(Site.site_id == site_in.site_id)
        .first()
    )

    if existing_site:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Site ID already exists.",
        )

    site = Site(
        site_id=site_in.site_id,
        name=site_in.name,
        country=site_in.country,
        region=site_in.region,
        district=site_in.district,
        latitude=site_in.latitude,
        longitude=site_in.longitude,
        site_type=site_in.site_type,
        status=site_in.status,
    )

    db.add(site)
    db.commit()
    db.refresh(site)

    return site