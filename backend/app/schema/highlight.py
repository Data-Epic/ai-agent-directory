from pydantic import BaseModel, Field
from typing import Optional 


class Highlight(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the highlight")
    user_id: int = Field(..., description="ID of the user who created the highlight")
    agent_name: str = Field(..., description="name of the agent associated with the highlight")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "agent_name": 'ai_agent_1'
            }
        }