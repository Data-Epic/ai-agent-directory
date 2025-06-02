from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ReviewCreateSchema(BaseModel):
    rating: int = Field(
        ..., ge=1, le=5, description="Rating given by the user (1 to 5)"
    )
    comment: Optional[str] = Field(
        None, max_length=1000, description="Comment provided by the user"
    )

    class Config:
        json_schema_extra = {
            "example": {"rating": 4, "comment": "Great agent, very helpful!"}
        }


class ReviewSchema(BaseModel):
    id: Optional[int] = Field(
        None, description="Unique identifier for the review"
    )
    user_id: UUID4 = Field(
        ..., description="ID of the user who created the review"
    )
    agent_name: str = Field(
        ..., description="Name of the agent associated with the review"
    )
    rating: int = Field(
        ..., ge=1, le=5, description="Rating given by the user (1 to 5)"
    )
    comment: Optional[str] = Field(
        None, max_length=1000, description="Comment provided by the user"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "agent_name": "ai_agent_1",
                "rating": 4,
                "comment": "Great agent, very helpful!",
            }
        }
