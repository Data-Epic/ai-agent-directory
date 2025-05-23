from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from  app.core.database import Base
import uuid


class Rating(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, default=uuid.uuid4)
    rating = Column(Integer, nullable=False, limit=5)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agent.id"), nullable=False)

    user=relationship("User", back_populates="ratings")