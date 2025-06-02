from schema.review import Review
from core.models.user import User
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi_pagination import Page, paginate, add_pagination
from auth.dependency import get_current_user

review_router = APIRouter()
add_pagination(review_router)

@review_router.post("/agents/{name}/review", response_model=Review, status_code=201, tags=["Reviews"])
async def submit_review(name: str, review_data:Review, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)) -> Review:
    """Submit a review for an agent."""
    existing_review = db.query(Review).filter(
        Review.user_id == user_data.user_id,
        Review.agent_name == name
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="Review already exists for this agent by this user")
    
    review_data.agent_name = name
    review_data.user_id = user_data.user_id

    db.add(review_data)
    db.commit()
    db.refresh(review_data)
    return review_data



@review_router.get("/agents/{name}/reviews", response_model=Page[Review], tags=["Reviews"])
async def list_reviews(name: str, db: Session = Depends(get_db)) -> Page[Review]:
    """List all reviews for an agent."""
    review = db.query(Review).filter(Review.agent_name == name).all()
    if not review:
        raise HTTPException(status_code=404, detail="No reviews found for this agent")
    return paginate(review)


