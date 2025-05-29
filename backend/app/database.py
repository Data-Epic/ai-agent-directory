"""
This module sets up the database connection using SQLAlchemy and provides
a session factory for database operations
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
path = Path(r"C:\Users\ayemi\OneDrive\Documents\yemi_agent\ai-agent-directory\backend\.env")

load_dotenv(dotenv_path=path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"{e}")


the_db = get_db()

# * Creating an additional function that gets the current user with jwt
def get_current_user(db = the_db, token = oauth2_scheme):
    from fastapi import HTTPException, status
    from jose import jwt

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # user_id = db.query(User).filter(User.id == payload.get("user_id")).first()
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")