from pydantic import BaseModel

class LayoutUpdateRequest(BaseModel):
    widgets_config: str  # JSON string
    accent_gradient: str | None = None
    font_size: str | None = None
    motion_enabled: bool | None = None

class LayoutOut(BaseModel):
    widgets_config: str
    accent_gradient: str
    font_size: str
    motion_enabled: bool

    model_config = {"from_attributes": True}

class StatsOverview(BaseModel):
    total_page_views: int
    total_project_views: int
    total_messages: int
    total_projects: int
