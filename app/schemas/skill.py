from pydantic import BaseModel

class SkillBase(BaseModel):
    name: str
    proficiency: int | None = None
    featured: bool = False
    order: int = 0

class SkillCreate(SkillBase):
    category_id: str

class SkillUpdate(BaseModel):
    name: str | None = None
    proficiency: int | None = None
    featured: bool | None = None
    order: int | None = None
    category_id: str | None = None

class SkillOut(SkillBase):
    id: str
    category_id: str

    model_config = {"from_attributes": True}

class SkillCategoryBase(BaseModel):
    name: str
    description: str | None = None
    order: int = 0

class SkillCategoryCreate(SkillCategoryBase):
    pass

class SkillCategoryOut(SkillCategoryBase):
    id: str
    skills: list[SkillOut] = []

    model_config = {"from_attributes": True}
