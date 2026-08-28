"""Main API router aggregating all endpoints."""

from fastapi import APIRouter
from .entities_api import router as entities_router
from .kb_api import router as kb_router
from .metrics_api import router as metrics_router
from .events_api import router as events_router

api_router = APIRouter(prefix="/api")

api_router.include_router(metrics_router)
api_router.include_router(entities_router)
api_router.include_router(kb_router)
api_router.include_router(events_router)

