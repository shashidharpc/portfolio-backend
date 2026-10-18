from datetime import datetime
from pydantic import BaseModel

class ProfileBase(BaseModel):
    full_name: str
    title: str
    headline: str
    bio: str
    location: str
    avatar_url: str | None = None
    resume_url: str | None = None
    available_for_hire: bool = True
    social_links: str | None = None

class ProfileUpdate(BaseModel):
    full_name: str | None = None
    title: str | None = None
    headline: str | None = None
    bio: str | None = None
    location: str | None = None
    avatar_url: str | None = None
    resume_url: str | None = None
    available_for_hire: bool | None = None
    social_links: str | None = None

class ProfileOut(ProfileBase):
    id: str
    updated_at: datetime

    model_config = {"from_attributes": True}
