from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.services.project_service import increment_project_views

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=list[ProjectOut])
def list_projects(
    category: Optional[str] = Query(None),
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Project).filter(Project.published == True)
    if category:
        query = query.filter(Project.category.ilike(f"%{category}%"))
    if featured_only:
        query = query.filter(Project.featured == True)
    return query.order_by(Project.order.asc()).all()

@router.get("/{slug}", response_model=ProjectOut)
def get_project(slug: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with slug '{slug}' not found"
        )
    return project

@router.post("/{slug}/view")
def register_view(slug: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    new_views = increment_project_views(db, project)
    return {"slug": slug, "views_count": new_views}

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    existing = db.query(Project).filter(Project.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already in use")
    
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.patch("/{id}", response_model=ProjectOut)
def update_project(
    id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    data = payload.model_dump(exclude_unset=True)
    for field, val in data.items():
        setattr(project, field, val)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    id: str,
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()
    return None
