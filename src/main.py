from __future__ import annotations
from fastapi import FastAPI
import redis.asyncio as redis

from .api import users, login, plants
from .core.redis_io import Redis as RedisIO
app = FastAPI(title="CannaTracker")

app.include_router(login.router)
app.include_router(users.router)
app.include_router(plants.router)


"""# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)"""
