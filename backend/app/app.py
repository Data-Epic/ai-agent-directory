import uvicorn
from fastapi import FastAPI
from core.database import Base, engine
from api.route.user import user_router
from api.route.agent import agent_router
from api.route.review import review_router
from api.route.highlight import highlight_router
from fastapi.middleware.cors import CORSMiddleware


from core.models.user import User
from core.models.agent import Agent
from core.models.highlight import Highlight
from core.models.rating import Rating
from core.models.review import Review



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

# Include routers
app.include_router(user_router, prefix="/api")
app.include_router(agent_router, prefix="/api")
app.include_router(review_router, prefix="/api")
app.include_router(highlight_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8090, reload=True, log_level="debug")
