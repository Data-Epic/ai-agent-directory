from sqlalchemy import String, Integer, Column, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class Rating(Base):
    __tablename__ = "ratings" 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False) 
    agent_name = Column(String, ForeignKey("agents.name", ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    agent = relationship("Agent", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "agent_name", name="_user_agent_rating_uc"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range")  
    )