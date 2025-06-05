import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from uuid import uuid4

from core.models.agent import Agent
from core.models.highlight import Highlight
from core.models.review import Review
from core.models.user import User


def test_create_user_object():
    user = User(
        id=uuid4(),
        first_name="Samuel",
        last_name="John",
        username="user123",
        email="user@example.com",
        hashed_password="Password122",
        is_admin=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert isinstance(user.id, uuid.UUID)
    assert user.first_name == "Samuel"
    assert user.last_name == "John"
    assert user.username == "user123"
    assert user.email == "user@example.com"
    assert user.hashed_password == "Password122"
    assert user.is_admin == 0
    assert user.created_at is not None
    assert user.updated_at is not None

    assert hasattr(user, "reviews")
    assert hasattr(user, "highlights")


def test_create_agent_object():
    agent = Agent(
        name="EcoWatch",
        description="A platform monitoring environmental data.",
        homepage_url="https://ecowatch.com",
        category="Environment",
        source="Satellite",
        trending=1,
    )

    assert agent.name == "EcoWatch"
    assert agent.description == "A platform monitoring environmental data."
    assert agent.homepage_url == "https://ecowatch.com"
    assert agent.category == "Environment"
    assert agent.source == "Satellite"
    assert agent.trending == 1

    assert agent.created_at is None
    assert agent.updated_at is None

    assert hasattr(agent, "highlights")
    assert hasattr(agent, "reviews")


def test_create_review_object():
    user_id = uuid4()

    review = Review(
        user_id=user_id,
        agent_name="EcoWatch",
        rating=4,
        comment="Very useful and accurate data.",
    )

    assert review.user_id == user_id
    assert review.agent_name == "EcoWatch"
    assert review.rating == 4
    assert review.comment == "Very useful and accurate data."

    assert hasattr(review, "user")
    assert review.user is None

    assert hasattr(review, "agent")
    assert review.agent is None


def test_create_highlight_object():
    user_id = uuid4()

    highlight = Highlight(user_id=user_id, agent_name="EcoWatch")

    assert highlight.user_id == user_id
    assert highlight.agent_name == "EcoWatch"

    assert hasattr(highlight, "user")
    assert highlight.user is None

    assert hasattr(highlight, "agent")
    assert highlight.agent is None

    constraint_names = [
        c.name for c in Highlight.__table_args__ if hasattr(c, "name")
    ]
    assert "_user_agent_highlight_uc" in constraint_names
