from pydantic import BaseModel

class ExperienceBase(BaseModel):
    role: str
    company: str
    location: str | None = None
    period: str
    description: str
    achievements: str | None = None  # JSON string array
    technologies: str | None = None  # JSON string array
    order: int = 0
    current: bool = False

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    role: str | None = None
    company: str | None = None
    location: str | None = None
    period: str | None = None
    description: str | None = None
    achievements: str | None = None
    technologies: str | None = None
    order: int | None = None
    current: bool | None = None

class ExperienceOut(ExperienceBase):
    id: str

    model_config = {"from_attributes": True}
