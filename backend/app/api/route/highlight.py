from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, get_current_user
from app.models import Highlight  # Assuming you have a Highlight model defined in models.py
from typing import List
from sqlalchemy.orm import Session
from app import schemas  # Assuming you have a schemas module for request/response models


router = APIRouter()

@router.post("/highlight")
def create_highlight(agent_id: int, db: Session = Depends(get_db), user =Depends(get_current_user)):
    """
    Create a new highlight.
    """
    highlight = Highlight(
        user_id=user.id,
        agent_id=agent_id  # Assuming current_user is a dependency that provides the current user's ID
        
    )
    db.add(highlight)
    db.commit()
    return highlight

@router.get("/highlights", response_model=List[schemas.AgentOut])
def list_highlights(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    List all highlights for the current user.
    """
    highlights = db.query(Highlight).filter(Highlight.user_id == get_current_user.id).all()
    if not highlights:
        raise HTTPException(status_code=404, detail="No highlights found")
    return highlights