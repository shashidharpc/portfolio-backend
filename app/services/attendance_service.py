from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.attendance import GeofenceZone, AttendanceRecord
from app.schemas.attendance import QRScanRequest, AttendanceVerificationResult
from app.services.geofence import is_within_geofence

def process_qr_attendance(
    db: Session,
    scan_data: QRScanRequest
) -> AttendanceVerificationResult:
    # 1. Fetch active geofence zones
    active_zones = db.query(GeofenceZone).filter(GeofenceZone.is_active == True).all()

    is_verified = False
    closest_distance = 999999.0
    matched_zone_name = None

    if not active_zones:
        # Default boundary if none configured in DB (Bengaluru tech hub coordinates)
        default_lat, default_lon, default_radius = 12.9716, 77.5946, 500.0
        inside, dist = is_within_geofence(
            scan_data.latitude,
            scan_data.longitude,
            default_lat,
            default_lon,
            default_radius
        )
        is_verified = inside
        closest_distance = dist
        matched_zone_name = "Default Campus Zone"
    else:
        for zone in active_zones:
            inside, dist = is_within_geofence(
                scan_data.latitude,
                scan_data.longitude,
                zone.latitude,
                zone.longitude,
                zone.radius_meters
            )
            if dist < closest_distance:
                closest_distance = dist
                matched_zone_name = zone.name
            if inside:
                is_verified = True
                matched_zone_name = zone.name
                break

    # 2. Record attendance in database
    record = AttendanceRecord(
        user_identifier=scan_data.user_identifier,
        device_id=scan_data.device_id,
        qr_token=scan_data.qr_token,
        latitude=scan_data.latitude,
        longitude=scan_data.longitude,
        is_verified=is_verified,
        verification_details=f"Distance: {closest_distance:.2f}m to {matched_zone_name}",
        timestamp=datetime.now(timezone.utc)
    )
    db.add(record)
    db.commit()

    message = (
        f"Attendance verified successfully within {matched_zone_name}."
        if is_verified
        else f"Location out of bounds ({closest_distance:.1f}m away from {matched_zone_name}). Attendance rejected."
    )

    return AttendanceVerificationResult(
        is_verified=is_verified,
        distance_meters=round(closest_distance, 2),
        zone_name=matched_zone_name,
        message=message,
        timestamp=record.timestamp
    )
