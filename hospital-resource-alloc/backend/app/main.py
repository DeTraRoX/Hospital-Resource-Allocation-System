from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .db import engine
from .routers import hospitals, requests, allocations, search, ws

app = FastAPI(title="Hospital Resource Allocation")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure tables exist (if not using Alembic yet)
def init_models():
    SQLModel.metadata.create_all(engine)

init_models()

# Routers
app.include_router(hospitals.router)
app.include_router(requests.router)
app.include_router(allocations.router)
app.include_router(search.router)
app.include_router(ws.router)
