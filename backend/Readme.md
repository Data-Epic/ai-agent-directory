https://www.youtube.com/watch?v=DBlmF91Accg
https://blog.devops.dev/level-up-your-development-workflow-with-pre-commit-and-github-actions-23b13f5efd6e

# 🧠 AI Agent Directory - Backend

A backend-first MVP platform for discovering and managing AI tools. Users can browse agents, save favorites, rate, and review them. Admins can manage visibility and trends. Built with **FastAPI** and **PostgreSQL**.

---

## 🚀 Features

### 👥 Authentication
- User signup/login with JWT
- Role-based access control (user vs. admin)

### 📦 Agent Management
- Browse agents by category
- View details for any agent
- Highlight (save) agents
- Submit reviews and ratings

### 🛠 Admin Functionality
- Toggle trending status on agents
- View analytics endpoints (top-rated, most highlighted)

### 🔄 Data Ingestion
- Seed agents from script
- Automated scheduled ETL supported

### 📑 Documentation
- Swagger UI at `/docs`
- ReDoc at `/redoc`

---

## 🧱 Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| DB | PostgreSQL |
| Auth | JWT + OAuth2 |
| Testing | Pytest |
| Container | Docker |
| CI/CD | GitHub Actions |
| Scheduler | `schedule` |

---
🗂 Project Structure
backend/
├── app/
│   ├── models.py         # SQLAlchemy models
│   ├── main.py           # FastAPI app entry
│   ├── auth.py           # JWT auth logic
│   ├── database.py       # DB connection/session
│   ├── deps.py           # Dependency injection (get_db, current_user)
│   ├── seed.py           # Agent seed script
│   ├── routers/
│   │   ├── users.py
│   │   ├── agents.py
│   │   ├── highlights.py
│   │   ├── reviews.py
│   │   ├── analytics.py
├── alembic/              # DB migrations
├── scripts/              # ETL scheduling script
├── tests/                # Pytest-based tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env

---
## 🗂 Project Structure

backend/
├── .github_workflows/
|  ├── precommit-hook.yml
|  ├── app/
|  |  ├── api/
|  |  |  ├── route/  # FastAPI app entry
|  |  |  |  ├── __init__.py
|  |  |  |  ├── agent.py
|  |  |  |  ├── highlight.py
|  |  |  |  ├── login.py  # JWT auth logic
|  |  |  |  ├── user.py
|  |  |  ├── schema/
|  |  |  |  ├── __init__.py
|  |  |  |  ├── validate.py
|  |  |  ├── utils/
|  |  |  |  ├── __init__.py
|  |  |  ├── core/
│  |  |  |  ├── models/  # SQLAlchemy models
|  |  |  |  |  ├── __init__.py
|  |  |  |  |  ├── agent.py
|  |  |  |  |  ├── highlight.py
|  |  |  |  |  ├── rating.py
|  |  |  |  |  ├── review.py
|  |  |  |  |  ├── user.py
│  |  |  |  ├── __init__.py
│  |  |  |  ├── database.py  # DB connection/session
|  |  |  ├── tests/
│  |  |  |  ├── test_models.py
|  |  ├── app.py
|  ├── .env
|  ├── .pre-commit-config.yaml
|  ├── Readme.md
|  ├── docker-compose.yml
|  ├── pyproject.toml
|  ├── pytest.ini

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-agent-directory.git
cd ai-agent-directory/backend

### 2. Create .env file

DATABASE_URL=postgresql://postgres:password@db:5432/ai_agents
SECRET_KEY=your-secret-key

### 3. Build and run using Docker Compose

docker-compose up --build

###  Running Tests

pytest tests/

## 📈 API Documentation
Swagger: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

## ✨ Example Endpoints
POST /auth/signup – Register a new user

POST /auth/login – Get a JWT token

GET /agents – List all AI agents

POST /agents/{id}/review – Submit a review

POST /agents/{id}/rate – Rate an agent

PATCH /admin/agents/{id}/toggle-trending – Admin-only
