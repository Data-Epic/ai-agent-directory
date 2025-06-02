"""FastAPI application entry point.
This module initializes the FastAPI application, sets up the database, and includes the
necessary routers for handling user, agent, review, and highlight routes.
"""

import uvicorn
from api.route.agent import agent_router
from api.route.highlight import highlight_router
from api.route.review import review_router
from api.route.user import user_router
from api.utils.create_initial_admin import create_initial_admin
from core.database import Base, engine
from core.models.agent import Agent  # noqa: F401
from core.models.highlight import Highlight  # noqa: F401
from core.models.review import Review  # noqa: F401
from core.models.user import User  # noqa: F401
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

app = FastAPI()


Base.metadata.create_all(bind=engine)

# Setup CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8090",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    create_initial_admin()


# Include routers
app.include_router(user_router, prefix="/api")
app.include_router(agent_router, prefix="/api")
app.include_router(review_router, prefix="/api")
app.include_router(highlight_router, prefix="/api")


add_pagination(app)


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="127.0.0.1", port=8090, reload=True, log_level="debug"
    )
