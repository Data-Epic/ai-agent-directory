from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas
from typing import List

router = APIRouter()


@router.get("/agent", response_model=List[schemas.AgentOut])
def list_agents(category: str = None, trending: bool = False or True, db: Session = Depends(get_db)):
    """
    List all agents.
    """
    query = db.query(Agent)
    if category:
        query = query.filter(Agent.category == category)
    if trending is not None:
        query = query.filter(Agent.trending == trending)
    
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No agents found")
    return results
    


@router.get("/agent/{agent_id}")
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific agent by ID.
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent