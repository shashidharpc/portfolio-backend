from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.models.attendance import AttendanceRecord, GeofenceZone
from app.schemas.attendance import QRScanRequest, AttendanceVerificationResult
from app.services.attendance_service import process_qr_attendance

router = APIRouter(prefix="/attendance", tags=["Attendance Automation"])

@router.post("/qr/scan", response_model=AttendanceVerificationResult)
def scan_qr_attendance(
    payload: QRScanRequest,
    db: Session = Depends(get_db)
):
    """
    Validates QR code submission alongside device GPS coordinates.
    Calculates Haversine distance against authorized campus geofences.
    """
    return process_qr_attendance(db, payload)

@router.get("/records")
def list_attendance_records(
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    return db.query(AttendanceRecord).order_by(AttendanceRecord.timestamp.desc()).limit(100).all()

@router.get("/zones")
def list_geofence_zones(db: Session = Depends(get_db)):
    return db.query(GeofenceZone).filter(GeofenceZone.is_active == True).all()
