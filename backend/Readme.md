# AI Agent Directory – Backend API
A **backend-first platform** serving as a **live, public directory of AI agents and tools**. Users can browse agents by category or trending status, register or log in, leave reviews, and save highlights. Admins can manage agents, including setting trending status. All data is accessible via a publicly documented REST API.

## Project Workflow Overview
![Capstone](images/Internship-Captstone.jpg)


## Live Deployment

* API: [`https://ai-agent-directory.onrender.com`](https://ai-agent-directory.onrender.com)
* API Docs: [`/docs`](https://ai-agent-directory.onrender.com/docs) | [`/redoc`](https://ai-agent-directory.onrender.com/redoc)

---
## Endpoint Images
[Endpoint Overview](images/image.png)


## Project Structure (Simplified)

```bash
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── alembic/
├── alembic.ini
├── app/
│   ├── api/
│   │   ├── route/
│   │   └── utils/
│   ├── auth/
│   ├── core/
│   │   └── models/
│   ├── schema/
│   └── tests/
├── .env (not tracked)
├── README.md
└── pytest.ini
```



## 🔧 Features

* **Live RESTful API** on [Render](https://render.com)
* **PostgreSQL** hosted on Render
* **API Documentation** via Swagger and ReDoc
* **JWT Authentication** with role-based authorization
* **Admin control** for trending agents
* **Highlights, Reviews, and Ratings**
* **Fully Dockerized Backend**
* **CI/CD** with GitHub Actions
* **Environment Variables** handled via `.env`
* **Over 20+ Automated Tests** using `pytest`
* **Modular & Clean Codebase**



## API Overview

### Users

| Endpoint      | Method | Description |
| ------------- | ------ | ----------- |
| `/api/signup` | POST   | Create User |
| `/api/login`  | POST   | Login User  |

### Admin

| Endpoint                              | Method | Description           |
| ------------------------------------- | ------ | --------------------- |
| `/api/admin/users/{username}/convert` | PATCH  | Convert User to Admin |
| `/api/admin/agents/{name}/trending`   | PATCH  | Update Agent Trending |

### Agents

| Endpoint                             | Method | Description            |
| ------------------------------------ | ------ | ---------------------- |
| `/api/agents/by-name/{name}`         | GET    | Get Agent by Name      |
| `/api/agents/by-category/{category}` | GET    | Get Agents by Category |
| `/api/agents/by-trends/{trending}`   | GET    | Get Trending Agents    |
| `/api/agents`                        | GET    | List All Agents        |

### Reviews

| Endpoint                           | Method | Description   |
| ---------------------------------- | ------ | ------------- |
| `/api/agents/{agent_name}/review`  | POST   | Submit Review |
| `/api/agents/{agent_name}/reviews` | GET    | Get Reviews   |

### Highlights

| Endpoint                         | Method | Description      |
| -------------------------------- | ------ | ---------------- |
| `/api/highlights/{agent_name}`   | POST   | Save Highlight   |
| `/api/highlights`                | GET    | List Highlights  |
| `/api/highlights/{highlight_id}` | DELETE | Delete Highlight |



## Dockerized Setup

To run the application in a fully Dockerized environment:

### 1. Clone the Repository

```bash
git clone https://github.com/data-epic/ai-agent-directory.git
cd ai-agent-directory
```

### 2. Create a `.env` File
Rename the `.env_example` file to `.env`, all local detials are there, you change it to your choice

### 3. Start the Application

```bash
docker-compose up --build
```
This will:

* Start the FastAPI backend
* Spin up a PostgreSQL database container
* Auto-run migrations via Alembic

### 4. Access the App

We expose our app to Port 8090 in our Docker Image
* Swagger UI: `http://localhost:8090/docs`
* ReDoc: `http://localhost:8090/redoc`

---

## Testing

```bash
pre-commit 
```

Over **20+ backend tests** are included, validating:
* Auth
* Models
* Routes
* Database



## Workflow
> Our software engineering team designed and developed the backend of this platform using **FastAPI**, focusing on API-first development. The goal is to provide a scalable, testable, and production-ready backend for a directory of AI agents.

CI/CD is powered by GitHub Actions to ensure clean merges, automated testing, and continuous delivery. Docker and Docker Compose ensure consistent local and cloud deployments.

*A sample image of our GitHub Actions pipeline will go here.*


## Docs & Contributing

* API Docs: [Swagger UI](https://ai-agent-directory.onrender.com/docs)
* For contributions, please fork the repo and submit a PR.
* Ensure to run tests and format with `black`, `isort`, and `pre-commit`.
