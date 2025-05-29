from fastapi import FastAPI
from app.api.route import user, agent, highlight

app = FastAPI()

app.include_router(user.router)
app.include_router(agent.router)
app.include_router(highlight.router)

