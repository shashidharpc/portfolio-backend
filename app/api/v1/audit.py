from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.models.audit_log import AuditLog, EventLog

router = APIRouter(prefix="/audit", tags=["Audit & Telemetry"])

@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()

@router.get("/event-logs")
def get_event_logs(
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    return db.query(EventLog).order_by(EventLog.created_at.desc()).limit(100).all()
