from schema.agent import Agent
from fastapi import APIRouter, HTTPException, Depends, status
from core.database import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page, paginate, add_pagination
from core.models.user import User
from auth.dependency import get_current_user


agent_router = APIRouter()
add_pagination(agent_router)

@agent_router.get("/agents/{name}", response_model=Agent, tags=["Agents"])
async def get_agent_by_name(name: str, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)) -> Page[Agent]:
    """Retrieve an agent by its name."""
    agent = db.query(Agent).filter(
        Agent.user_id == user_data.user_id,
        Agent.name == name).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@agent_router.get("/agents/{category}", response_model=Agent, tags=["Agents"])
async def get_agent_category(category: str, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)) -> Page[Agent]:
    """Retrieve an agent by category."""
    agent = db.query(Agent).filter(
        Agent.user_id == user_data.user_id,
        Agent.category == category).all()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent category not found")
    return paginate(agent)

@agent_router.get("agents/{trending}", response_model=Agent, tags=["Agents"])
async def get_agent_trending(trending: bool, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)) -> Page[Agent]:
    """Retrieve agents that are trending."""
    agent = db.query(Agent).filter(
        Agent.user_id == user_data.user_id,
        Agent.trending == trending).all()
    if not agent:
        raise HTTPException(status_code=404, detail="No trending agents found")
    return paginate(agent)


@agent_router.get("/agents", response_model=Page[Agent], tags=["Agents"])
async def list_agents(db: Session = Depends(get_db)) -> Page[Agent]:
    """List all agents."""
    agent = db.query(Agent).all()
    if not agent:
        raise HTTPException(status_code=404, detail="No agents found")
    return paginate(agent)


@agent_router.patch("/agents/{name}/trending", response_model=Agent, tags=["Agents"])
async def update_agent_trending(
    name: str,
    agent_data: Agent,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
) -> Agent:
    """Allow only admin to update an agent's trending status."""

    if not user_data.is_Admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )

    agent = db.query(Agent).filter(Agent.name == name).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent.trending = agent_data.trending
    db.commit()
    db.refresh(agent)

    return agent