import os
import sys
from datetime import datetime
from urllib.parse import quote

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_pagination import add_pagination
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["DATABASE_URL"] = "sqlite:///"
os.environ["TESTING"] = "true"

# Import app and database components
from core.database import Base, get_db
from core.models.agent import Agent
from core.models.user import User
from core.models.review import Review
from core.models.highlight import Highlight
from auth.dependency import get_current_user, require_admin
from api.route.agent import agent_router


TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)



@pytest.fixture(scope="function")
def test_session():
    """Create a session with a shared in-memory database connection."""
    connection = test_engine.connect()
    transaction = connection.begin()
    

    Base.metadata.create_all(bind=connection)

    session = TestingSessionLocal(bind=connection)

    try:
        sample_agents = [
            Agent(
                name="Jasper.ai",
                description="AI content creation platform for marketing copy and campaigns",
                homepage_url="https://www.jasper.ai/",
                category="Marketing",
                source="Jasper",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                trending=True,
            ),
            Agent(
                name="Copy.ai",
                description="AI-powered copywriting assistant for marketing content",
                homepage_url="https://www.copy.ai/",
                category="Marketing",
                source="Copy.ai",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                trending=False
            ),
        ]
        session.add_all(sample_agents)
        session.commit()

        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_app():
    """Create a fresh FastAPI app with the agent router for testing."""
    app = FastAPI()
    app.include_router(agent_router, prefix="/api")
    add_pagination(app)
    return app

@pytest.fixture(scope="function")
def client(test_session, test_app):
    """Provide a test client with overridden dependencies."""
    def override_get_db():
        yield test_session
       
    def mock_get_current_user():
        return User(
            id=1,
            username="testuser",
            email="test@example.com",
            is_admin=False
        )
    
    def mock_admin_user():
        mock_user = User(
            id=1,
            username="admin",
            email="admin@example.com",
            is_admin=True
        )
        return mock_user

  
    test_app.dependency_overrides[get_db] = override_get_db
    test_app.dependency_overrides[get_current_user] = mock_get_current_user
    test_app.dependency_overrides[require_admin] = mock_admin_user

    with TestClient(test_app) as c:
        yield c

    test_app.dependency_overrides.clear()



def test_get_agent_by_name_found(client):
    encoded_name = quote("Jasper.ai")
    response = client.get(f"/api/agents/by-name/{encoded_name}")

    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jasper.ai"
    assert data["category"] == "Marketing"

def test_get_agents_by_category_found(client):
    category = "Marketing"
    response = client.get(f"/api/agents/by-category/{category}")

    print(f"Status: {response.status_code}, Content: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert all(agent["category"] == category for agent in data["items"])

def test_get_trending_agents_found(client):
    trending = 1
    response = client.get(f"/api/agents/by-trends/{trending}")

    print(f"Status: {response.status_code}, Content: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert all(agent["trending"] == trending for agent in data["items"])


def test_list_agents(client):
    response = client.get("/api/agents")

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_update_agent_trending_success(client):
    name = "Jasper.ai"
    payload = {"trending": 1}

    response = client.patch(f"/api/admin/agents/{quote(name)}/trending", json=payload)

    print(f"Status: {response.status_code}, Content: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name
    assert data["trending"] == 1

