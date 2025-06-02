from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class Highlight(Base):
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False) 
    agent_name = Column(String, ForeignKey("agents.name"), nullable=False)
    
    user = relationship("User", back_populates="highlights")
    agent = relationship("Agent", back_populates="highlights")

    __table_args__ = (
        UniqueConstraint("user_id", "agent_name", name="_user_agent_highlight_uc"),
    )
