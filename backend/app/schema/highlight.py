from pydantic import UUID4, BaseModel, Field


class HighlightCreateSchema(BaseModel):
    agent_name: str = Field(
        ..., description="Name of the agent associated with the highlight"
    )


class HighlightSchema(BaseModel):
    id: int = Field(..., description="Unique identifier for the highlight")
    user_id: UUID4 = Field(
        ..., description="ID of the user who created the highlight"
    )
    agent_name: str = Field(
        ..., description="Name of the agent associated with the highlight"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "agent_name": "ai_agent_1",
            }
        }
