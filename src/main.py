from __future__ import annotations
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import users, plants, templates
app = FastAPI(title="CannaTracker")

app.include_router(users.router)
app.include_router(plants.router)
app.include_router(templates.router)


# CORS
origins = [
    "http://localhost:5173",
    "https://kind-grass-0c965211e.5.azurestaticapps.net"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
