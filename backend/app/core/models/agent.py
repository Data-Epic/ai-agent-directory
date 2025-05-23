from sqlalchemy import String, Integer, Column, VARCHAR, DateTime
from sqlalchemy.orm import relationship
from  app.core.database import Base

class Agent(Base):
    __tablename__ = "agents"

    
    name = Column(String, unique=True, index=True)
    descritpion = Column(VARCHAR(1000))
    homepage_url = Column(VARCHAR(100))
    category = Column(VARCHAR(1000))
    sournce = Column(VARCHAR(1000))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    posts = relationship("Post", back_populates="username")