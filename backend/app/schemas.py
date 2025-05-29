from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


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


class HighlightOut(BaseModel):
    user_id: int
    agent_id: int

    class Config:
        orm_mode = True
