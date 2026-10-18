from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageOut

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def submit_contact_form(
    payload: MessageCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(",")[0].strip() if forwarded else request.client.host if request.client else None

    message = Message(
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        content=payload.content,
        ip=client_ip
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("", response_model=list[MessageOut])
def get_inbox_messages(
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    return db.query(Message).order_by(Message.created_at.desc()).all()

@router.patch("/{id}/read", response_model=MessageOut)
def mark_message_read(
    id: str,
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    msg = db.query(Message).filter(Message.id == id).first()
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    msg.is_read = True
    db.commit()
    db.refresh(msg)
    return msg

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    id: str,
    db: Session = Depends(get_db),
    _admin = Depends(require_admin)
):
    msg = db.query(Message).filter(Message.id == id).first()
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    db.delete(msg)
    db.commit()
    return None
