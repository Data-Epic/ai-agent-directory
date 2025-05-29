from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# ----------------------------
# User
# ----------------------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True

# ----------------------------
# Agent
# ----------------------------

class AgentBase(BaseModel):
    name: str
    category: str
    description: Optional[str]
    url: str

class AgentOut(AgentBase):
    id: int
    is_trending: bool
    average_rating: Optional[float]

    class Config:
        orm_mode = True

# ----------------------------
# Review
# ----------------------------

class ReviewCreate(BaseModel):
    content: str

class ReviewOut(BaseModel):
    id: int
    user_id: int
    agent_id: int
    content: str

    class Config:
        orm_mode = True

# ----------------------------
# Rating
# ----------------------------

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)

class RatingOut(BaseModel):
    id: int
    user_id: int
    agent_id: int
    score: int

    class Config:
        orm_mode = True

# ----------------------------
# Highlight
# ----------------------------

class HighlightOut(BaseModel):
    user_id: int
    agent_id: int

    class Config:
        orm_mode = True
