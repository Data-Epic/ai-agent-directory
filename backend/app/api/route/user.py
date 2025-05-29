# creating the endpoints for login and signup
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import User  # Assuming you have a User model defined in models.py
from app.database import get_db  # Assuming you have a get_db function in database.py
from app.api import utils
from app import models, schemas   # Assuming you have a schemas module for request/response models
router = APIRouter()


# * Creating endpoints for login and signup
# !Sample code for login and signup endpoints using FastAPI
# !Code will still be altered to fit the use case of the database and authentication system with jwt tokens
# Models for request validatio

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    User signup endpoint.
    """
    # Here you would typically hash the password and save the user to the database
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the password (you can use a library like bcrypt)
    hash_password = utils.hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password
    )
    db.add(new_user)
    db.commit()
    
    return new_user
