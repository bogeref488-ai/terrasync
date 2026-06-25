from fastapi import APIRouter

from app.api.v1.routers import health, sites, work_orders, templates, reports, defects

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(sites.router)
api_router.include_router(work_orders.router)
api_router.include_router(templates.router)
api_router.include_router(reports.router)
api_router.include_router(defects.router)
