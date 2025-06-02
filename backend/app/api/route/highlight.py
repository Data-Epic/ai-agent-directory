from auth.dependency import get_current_user
from core.database import get_db
from core.models.highlight import Highlight
from core.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, add_pagination, paginate
from schema.highlight import HighlightCreateSchema, HighlightSchema
from sqlalchemy.orm import Session

highlight_router = APIRouter()
add_pagination(highlight_router)


@highlight_router.post(
    "/highlights/{agent_name}",
    response_model=HighlightSchema,
    status_code=201,
    tags=["Highlights"],
)
async def save_highlight(
    highlight_data: HighlightCreateSchema,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user),
) -> HighlightSchema:
    existing_highlight = (
        db.query(Highlight)
        .filter(
            Highlight.user_id == user_data.id,
            Highlight.agent_name == highlight_data.agent_name,
        )
        .first()
    )
    if existing_highlight:
        raise HTTPException(status_code=400, detail="Highlight already exists")

    new_highlight = Highlight(
        user_id=user_data.id, agent_name=highlight_data.agent_name
    )

    db.add(new_highlight)
    db.commit()
    db.refresh(new_highlight)

    return new_highlight


@highlight_router.get(
    "/highlights", response_model=Page[HighlightSchema], tags=["Highlights"]
)
async def list_highlights(
    db: Session = Depends(get_db), user_data: User = Depends(get_current_user)
) -> Page[HighlightSchema]:
    highlights = db.query(Highlight).filter().all()

    if not highlights:
        raise HTTPException(
            status_code=404,
            detail="No highlighted AI agents found for this user",
        )

    return paginate(highlights)


@highlight_router.delete(
    "/highlights/{highlight_id}", status_code=204, tags=["Highlights"]
)
async def delete_highlight(
    highlight_id: int,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user),
):
    highlight = (
        db.query(Highlight)
        .filter(
            Highlight.user_id == user_data.id, Highlight.id == highlight_id
        )
        .first()
    )

    if not highlight:
        raise HTTPException(status_code=404, detail="Highlight not found")

    db.delete(highlight)
    db.commit()

    return status.HTTP_204_NO_CONTENT
