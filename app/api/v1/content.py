from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.models.profile import Profile
from app.models.skill import SkillCategory, Skill
from app.models.experience import Experience
from app.schemas.profile import ProfileOut, ProfileUpdate
from app.schemas.skill import SkillCategoryOut
from app.schemas.experience import ExperienceOut

router = APIRouter(prefix="/content", tags=["Content"])

@router.get("/profile", response_model=ProfileOut)
def get_public_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == "default").first()
    if not profile:
        profile = Profile(
            id="default",
            full_name="Shashidhar P C",
            title="Full Stack Software Engineer",
            headline="Developing secure, database-driven web applications using Python, Flask, JavaScript, and PHP.",
            bio="Full Stack Software Engineer based in Bengaluru with a strong foundation in Data Structures, Algorithms, Object Oriented Design, and the full Software Development Life Cycle (SDLC).",
            location="Bengaluru, Karnataka, India",
            available_for_hire=True
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.patch("/profile", response_model=ProfileOut)
def update_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    profile = db.query(Profile).filter(Profile.id == "default").first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    data = payload.model_dump(exclude_unset=True)
    for field, val in data.items():
        setattr(profile, field, val)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/skills", response_model=list[SkillCategoryOut])
def list_skills(db: Session = Depends(get_db)):
    return db.query(SkillCategory).order_by(SkillCategory.order.asc()).all()

@router.get("/experiences", response_model=list[ExperienceOut])
def list_experiences(db: Session = Depends(get_db)):
    return db.query(Experience).order_by(Experience.order.asc()).all()
