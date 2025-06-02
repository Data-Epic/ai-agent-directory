from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False) 
    agent_name = Column(String, ForeignKey("agents.name", ondelete="CASCADE"), nullable=False)
    review = Column(VARCHAR(120), nullable=False)

    user = relationship("User", back_populates="reviews")  
    agent = relationship("Agent", back_populates="reviews")
