from datetime import datetime
from pydantic import BaseModel

class ProjectBase(BaseModel):
    slug: str
    title: str
    tagline: str | None = None
    description: str
    content: str | None = None
    cover_image: str
    images: str | None = None  # JSON array
    category: str
    technologies: str  # JSON array
    metrics: str | None = None  # JSON metrics
    github_url: str | None = None
    live_url: str | None = None
    featured: bool = False
    published: bool = True
    order: int = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    slug: str | None = None
    title: str | None = None
    tagline: str | None = None
    description: str | None = None
    content: str | None = None
    cover_image: str | None = None
    images: str | None = None
    category: str | None = None
    technologies: str | None = None
    metrics: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    featured: bool | None = None
    published: bool | None = None
    order: int | None = None

class ProjectOut(ProjectBase):
    id: str
    views_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
