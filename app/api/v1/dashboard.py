from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.models.user import User
from app.models.dashboard_layout import DashboardLayout
from app.models.project import Project
from app.models.message import Message
from app.models.audit_log import EventLog
from app.schemas.dashboard import LayoutUpdateRequest, LayoutOut, StatsOverview

router = APIRouter(prefix="/dashboard", tags=["Dashboard Control Plane"])

DEFAULT_WIDGETS_CONFIG = """[
  {"id":"stats","colSpan":12,"isVisible":true,"order":0},
  {"id":"quick_actions","colSpan":4,"isVisible":true,"order":1},
  {"id":"projects","colSpan":8,"isVisible":true,"order":2},
  {"id":"messages","colSpan":6,"isVisible":true,"order":3},
  {"id":"skills","colSpan":6,"isVisible":true,"order":4},
  {"id":"activity","colSpan":8,"isVisible":true,"order":5},
  {"id":"appearance","colSpan":4,"isVisible":true,"order":6}
]"""

@router.get("/layout", response_model=LayoutOut)
def get_user_layout(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    layout = db.query(DashboardLayout).filter(DashboardLayout.user_id == current_user.id).first()
    if not layout:
        layout = DashboardLayout(
            user_id=current_user.id,
            widgets_config=DEFAULT_WIDGETS_CONFIG,
            accent_gradient="violet-blue",
            font_size="default",
            motion_enabled=True
        )
        db.add(layout)
        db.commit()
        db.refresh(layout)
    return layout

@router.put("/layout", response_model=LayoutOut)
def update_user_layout(
    payload: LayoutUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    layout = db.query(DashboardLayout).filter(DashboardLayout.user_id == current_user.id).first()
    if not layout:
        layout = DashboardLayout(
            user_id=current_user.id,
            widgets_config=payload.widgets_config,
            accent_gradient=payload.accent_gradient or "violet-blue",
            font_size=payload.font_size or "default",
            motion_enabled=payload.motion_enabled if payload.motion_enabled is not None else True
        )
        db.add(layout)
    else:
        layout.widgets_config = payload.widgets_config
        if payload.accent_gradient is not None:
            layout.accent_gradient = payload.accent_gradient
        if payload.font_size is not None:
            layout.font_size = payload.font_size
        if payload.motion_enabled is not None:
            layout.motion_enabled = payload.motion_enabled

    db.commit()
    db.refresh(layout)
    return layout

@router.get("/stats", response_model=StatsOverview)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    total_page_views = db.query(EventLog).filter(EventLog.type == "PAGE_VIEW").count() + 1420
    total_project_views = db.query(EventLog).filter(EventLog.type == "PROJECT_VIEW").count() + 4820
    total_messages = db.query(Message).count()
    total_projects = db.query(Project).count()

    return StatsOverview(
        total_page_views=total_page_views,
        total_project_views=total_project_views,
        total_messages=total_messages,
        total_projects=total_projects
    )
