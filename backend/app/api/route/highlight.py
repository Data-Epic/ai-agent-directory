from schema.highlight import Highlight
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi_pagination import Page, paginate, add_pagination
from core.models.user import User
from auth.dependency import get_current_user


highlight_router = APIRouter()
add_pagination(highlight_router)


@highlight_router.post("/highlights/{agent}", response_model=Highlight, status_code=201, tags=["Highlights"])
async def save_highlight(highlight_data: Highlight, 
                         db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Highlight:
    """Save an agent to user highlights."""
    existing_highlight = db.query(Highlight).filter(
        Highlight.user_id == current_user.user_id,
        Highlight.agent_id == Highlight.agent_id
    ).first()
    
    if existing_highlight:
        raise HTTPException(status_code=400, detail="Highlight already exists")
    
    db.add(highlight_data)
    db.commit()
    db.refresh(highlight_data)
    return highlight_data

@highlight_router.get("/highlights", response_model=Page[Highlight], tags=["Highlights"])
async def list_highlights(db: Session = Depends(get_db), user_data: User = Depends(get_current_user)) -> Page[Highlight]:
    """List user’s saved agents."""
    highlight = db.query(Highlight).filter(Highlight.user_id == user_data.user_id).all()
    if not highlight:
        raise HTTPException(status_code=404, detail="No highlighted AI agent found for this user")
    return paginate(highlight)


@highlight_router.delete("/highlights/{highlight_id}", status_code=204, tags=["Highlights"])
async def delete_highlight(highlight_id:int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    """Delete a highlight by ID."""
    highlight = db.query(Highlight).filter(
        Highlight.user_id == current_user.user_id,
        Highlight.id == highlight_id).first()
    if not highlight:
        raise HTTPException(status_code=204, detail="Highlight not found")
    
    db.delete(highlight)
    db.commit()
    return status.HTTP_204_NO_CONTENT