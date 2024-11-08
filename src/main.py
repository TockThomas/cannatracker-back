from __future__ import annotations
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import users, plants, templates, friends
from src.core.redis_io import Redis, redis_connection

app = FastAPI(title="CannaTracker")

app.include_router(users.router, prefix="/api")
app.include_router(plants.router, prefix="/api")
app.include_router(friends.router, prefix="/api")
app.include_router(templates.router, prefix="/api")

@app.on_event("startup")
async def startup():
    redis = redis_connection()
    await redis.init_db()


# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://kind-grass-0c965211e.5.azurestaticapps.net",
    "https://www.thegreenwizard.live",
    "https://thegreenwizard.live"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
