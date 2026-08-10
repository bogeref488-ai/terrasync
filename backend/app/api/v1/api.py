from fastapi import APIRouter

from app.api.v1.routers import auth
from app.api.v1.routers import defects
from app.api.v1.routers import inspection_templates
from app.api.v1.routers import reports
from app.api.v1.routers import sites
from app.api.v1.routers import work_orders


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(work_orders.router, prefix="/work-orders", tags=["work orders"])
api_router.include_router(
    inspection_templates.router,
    prefix="/inspection-templates",
    tags=["inspection templates"],
)
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(defects.router, prefix="/defects", tags=["defects"])