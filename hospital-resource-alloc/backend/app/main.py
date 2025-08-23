from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, select
from pathlib import Path

# Import engine and models using absolute paths
from app.db import engine
from app.models import Hospital

# Import your routers using absolute paths
from app.routers import hospitals, requests, allocations, search, ws


# ----------------------------------------------------
# App setup
# ----------------------------------------------------
app = FastAPI(title="Hospital Resource Allocation")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base paths
BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"

# Optional: serve static files if needed
# app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# ----------------------------------------------------
# DB Init + Seed (Ensure only one hospital exists)
# ----------------------------------------------------
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        hospital = session.exec(select(Hospital).where(Hospital.id == 1)).first()
        if not hospital:
            hospital = Hospital(
                id=1,
                name="City Hospital",
                total_beds=5,
                available_beds=5,
                ventilators=5,
                available_ventilators=5,
            )
            session.add(hospital)
            session.commit()
            print("✅ Default Hospital (ID=1) created")
        else:
            print("ℹ️ Hospital (ID=1) already exists")


# ----------------------------------------------------
# Routers
# ----------------------------------------------------
app.include_router(hospitals.router)
app.include_router(requests.router)
app.include_router(allocations.router)
app.include_router(search.router)
app.include_router(ws.router)


# ----------------------------------------------------
# Routes
# ----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    if not INDEX_FILE.exists():
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)
    return INDEX_FILE.read_text(encoding="utf-8")
