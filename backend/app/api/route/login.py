# creating the endpoints for login and signup
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models import User  # Assuming you have a User model defined in models.py
from app.database import get_db
from app import schemas, utils, models  # Assuming you have a schemas module for request/response models
from sqlalchemy.orm import Session # Assuming you have a get_db function in database.py


router = APIRouter()


# * Creating endpoints for login and signup
# !Sample code for login and signup endpoints using FastAPI
# !Code will still be altered to fit the use case of the database and authentication system with jwt tokens
# Models for request validatio

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    User login endpoint.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Verify the password (you can use a library like bcrypt)
    if not utils.verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Generate a JWT token (you can use a library like PyJWT)
    token = utils.create_jwt(user_id=existing_user.id)
    if not token:
        raise HTTPException(status_code=500, detail="Could not create token")
    
    return {"message": "Login successful", "token": token}