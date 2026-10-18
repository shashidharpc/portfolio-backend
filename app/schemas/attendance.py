from datetime import datetime
from pydantic import BaseModel

class QRScanRequest(BaseModel):
    user_identifier: str
    qr_token: str
    latitude: float
    longitude: float
    device_id: str | None = None

class AttendanceVerificationResult(BaseModel):
    is_verified: bool
    distance_meters: float
    zone_name: str | None = None
    message: str
    timestamp: datetime
