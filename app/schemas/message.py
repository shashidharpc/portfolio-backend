from datetime import datetime
from pydantic import BaseModel, EmailStr

class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str | None = None
    content: str

class MessageOut(BaseModel):
    id: str
    name: str
    email: str
    subject: str | None = None
    content: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
