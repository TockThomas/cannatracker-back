from __future__ import annotations
from fastapi import FastAPI
import redis.asyncio as redis
from starlette.middleware.cors import CORSMiddleware

from .api import users, plants, templates
from .core.redis_io import Redis as RedisIO

app = FastAPI(title="CannaTracker")

app.include_router(users.router)
app.include_router(plants.router)
app.include_router(templates.router)


# CORS
origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
