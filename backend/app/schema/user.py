from pydantic import BaseModel, EmailStr, Field, UUID4



class CreateUser(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    password: str = Field(..., min_length=8, description="User's password")

class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Type of the token, usually 'bearer'")