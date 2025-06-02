from auth.dependency import get_current_user
from core.database import get_db
from core.models.review import Review
from core.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from schema.review import ReviewCreateSchema, ReviewSchema
from sqlalchemy.orm import Session

review_router = APIRouter(prefix="/agents", tags=["Reviews"])
add_pagination(review_router)


@review_router.post(
    "/agents/{agent_name}/review", response_model=ReviewSchema, status_code=201
)
async def create_review(
    agent_name: str,
    review_in: ReviewCreateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = (
        db.query(Review)
        .filter(Review.agent_name == agent_name, Review.user_id == user.id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Review already exists for this agent by this user",
        )

    new_review = Review(
        agent_name=agent_name,
        user_id=user.id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@review_router.get("/{agent_name}/reviews", response_model=Page[ReviewSchema])
async def get_reviews(
    agent_name: str,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user),
) -> Page[ReviewSchema]:
    """List all reviews for a specific agent."""

    reviews = db.query(Review).filter(Review.agent_name == agent_name).all()
    if not reviews:
        raise HTTPException(
            status_code=404, detail="No reviews found for this agent"
        )

    return paginate(reviews)
