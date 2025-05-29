from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    highlights = relationship("Highlight", back_populates="user")

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(Text)
    trending = Column(Boolean, default=False)

class Highlight(Base):
    __tablename__ = "highlights"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), primary_key=True)
    user = relationship("User", back_populates="highlights")
    agent = relationship("Agent")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    content = Column(Text)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    value = Column(Float)

