from app.core.database import get_db
from sqlalchemy.orm import Session




def test_get_db():
    db = next(get_db())
    
    assert isinstance(db, Session), "get_db should return a SQLAlchemy Session object"
    
    # Ensure the session is properly closed after use
    db.close()
    
    # Check if the session is closed
    assert db.is_active is False, "The database session should be closed after use"