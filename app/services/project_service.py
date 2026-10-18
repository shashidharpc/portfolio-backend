from typing import Optional
from sqlalchemy.orm import Session
from app.models.project import Project

def get_project_by_slug(db: Session, slug: str) -> Optional[Project]:
    return db.query(Project).filter(Project.slug == slug).first()

def increment_project_views(db: Session, project: Project) -> int:
    project.views_count += 1
    db.commit()
    db.refresh(project)
    return project.views_count
