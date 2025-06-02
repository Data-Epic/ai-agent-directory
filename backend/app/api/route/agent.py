from auth.dependency import get_current_user, require_admin
from core.database import get_db
from core.models.agent import Agent
from core.models.user import User
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_pagination import Page, add_pagination, paginate
from schema.agent import (
    AgentSchema,
    AgentTrendingResponse,
    AgentTrendingUpdate,
)
from sqlalchemy.orm import Session

agent_router = APIRouter()
add_pagination(agent_router)


@agent_router.get(
    "/agents/by-name/{name}", response_model=AgentSchema, tags=["Agents"]
)
async def get_agent_by_name(
    name: str,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user),
) -> AgentSchema:
    """Retrieve an agent by name."""
    agent = db.query(Agent).filter(Agent.name == name).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@agent_router.get(
    "/agents/by-category/{category}",
    response_model=Page[AgentSchema],
    tags=["Agents"],
)
async def get_agents_by_category(
    category: str,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user),
) -> Page[AgentSchema]:
    """Retrieve agents by category."""
    agents = db.query(Agent).filter(Agent.category == category).all()
    if not agents:
        raise HTTPException(
            status_code=404, detail="No agents found for this category"
        )
    return paginate(agents)


@agent_router.get(
    "/agents/by-trends/{trending}",
    response_model=Page[AgentSchema],
    tags=["Agents"],
)
async def get_trending_agents(
    trending: int = Path(
        ..., ge=0, le=1, description="Use 1 for trending, 0 for not trending"
    ),
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user),
) -> Page[AgentSchema]:
    """Retrieve agents based on trending value (1 or 0)."""
    agents = db.query(Agent).filter(Agent.trending == trending).all()
    if not agents:
        raise HTTPException(status_code=404, detail="No matching agents found")
    return paginate(agents)


@agent_router.get("/agents", response_model=Page[AgentSchema], tags=["Agents"])
async def list_agents(
    db: Session = Depends(get_db), user_data: User = Depends(get_current_user)
) -> Page[AgentSchema]:
    """List all agents."""
    agents = db.query(Agent).all()
    if not agents:
        raise HTTPException(status_code=404, detail="No agents found")
    return paginate(agents)


@agent_router.patch(
    "/admin/agents/{name}/trending",
    response_model=AgentTrendingResponse,
    tags=["Admin"],
)
async def update_agent_trending(
    name: str,
    agent_data: AgentTrendingUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
) -> AgentTrendingResponse:
    agent = db.query(Agent).filter(Agent.name == name).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent.trending = int(agent_data.trending)

    db.commit()
    db.refresh(agent)

    return agent
