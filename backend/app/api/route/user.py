from fastapi import APIRouter, Depends, HTTPException   
from sqlalchemy.orm import Session
from core.models.user import User
from core.database import get_db
from schema.user import CreateUser,UserResponse, UserLogin, Token
from auth.auth import hashed_password,verify_password,generate_token
from auth.dependency import get_current_user
from sqlalchemy import or_



user_router = APIRouter()


@user_router.post("/signup", response_model=UserResponse, status_code=201, tags=["User"], description="Create a new user")
async def create_user(user_data: CreateUser, db: Session = Depends(get_db)):
    """Create a new user in the database."""

    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password(user_data.password)  
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.post("/login", response_model=Token, status_code=200, tags=["User"], description="Login a user")
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login a user by checking credentials."""
    user = db.query(User).filter(
    or_(
        User.username == getattr(user_data, "username", None),
        User.email == getattr(user_data, "email", None)
    )
    ).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = generate_token(data={"id": str(user.id)})
    return Token(access_token=token, token_type="bearer")


@user_router.patch("/users/{user_id}/toggle_admin", response_model=UserResponse, tags=["User"], description="Toggle Admin Status of a User")
async def toggle_admin_status(user_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    """Toggle Admin Status of a User."""
    if not user_data.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_admin = 0 if user.is_admin else 1  
    db.commit()
    db.refresh(user)
    return user
