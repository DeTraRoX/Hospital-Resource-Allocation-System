from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Ensure tables exist
def init_models():
    SQLModel.metadata.create_all(engine)

init_models()

# Routers
app.include_router(hospitals.router)
app.include_router(requests.router)
app.include_router(allocations.router)
app.include_router(search.router)
app.include_router(ws.router)

# Static + Templates setup
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")
templates = Jinja2Templates(directory="backend/app/templates")

# Home route (serve index.html)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
