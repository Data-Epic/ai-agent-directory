# models/user.py
import os
import uuid

from core.database import Base
from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete"
    )
    highlights = relationship(
        "Highlight", back_populates="user", cascade="all, delete"
    )
