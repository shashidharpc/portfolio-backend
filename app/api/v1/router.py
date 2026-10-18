from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.projects import router as projects_router
from app.api.v1.messages import router as messages_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.content import router as content_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.audit import router as audit_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(messages_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(content_router)
api_v1_router.include_router(attendance_router)
api_v1_router.include_router(audit_router)
