"""
Agent model for the application.
This model represents an agent with various attributes such as name, description, homepage URL, category, and source.

https://docs.sqlalchemy.org/en/14/core/defaults.html#client-invoked-sql-expressions
"""

from sqlalchemy import (
    String, Integer, Column, VARCHAR, DateTime,
    func)
from sqlalchemy.orm import relationship
from core.database import Base  


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(VARCHAR(1000)) 
    homepage_url = Column(VARCHAR(100))
    category = Column(VARCHAR(1000))
    source = Column(VARCHAR(1000)) 
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  

    highlights = relationship("Highlight", back_populates="agent")
    ratings = relationship("Rating", back_populates="agent")
    reviews = relationship("Review", back_populates="agent")
