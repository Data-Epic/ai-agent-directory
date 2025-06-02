import os

import jwt
from auth.bearer import JWTBearer
from core.database import SessionLocal
from core.models.user import User
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(JWTBearer())) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_admin != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
