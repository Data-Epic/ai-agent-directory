from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from  app.core.database import Base
from datetime import datetime, timedelta
import uuid
import bcrypt
import jwt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, deafult=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="username")

    def hashed_password(self, password: str):
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                                          bcrypt.gensalt().decode('utf-8'))
                                                          
    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def generate_token(self):
        expiration = datetime.timezone.utcnow() + timedelta(hours=24)
        payload = {
            "sub": self.id,
            "ex": expiration,
        }

        return jwt.encode(payload,"", algorithm="HS256")
