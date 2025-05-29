from fastapi import APIRouter, Depends, HTTPException
from database import get_db


router = APIRouter()


@router.get("/agent")
def list_agents(category: str = None, trending: bool = False or True, db: Depends = get_db):
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
def get_agent(agent_id: int):
    """
    Get details of a specific agent by ID.
    """
    # * Sample data for agents
    agents = {
        1: {"id": 1, "name": "Agent 1", "category": "Category A", "trending": True},
        2: {"id": 2, "name": "Agent 2", "category": "Category B", "trending": False},
        3: {"id": 3, "name": "Agent 3", "category": "Category C", "trending": True}
    }
    
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent