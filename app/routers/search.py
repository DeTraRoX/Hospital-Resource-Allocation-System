from fastapi import APIRouter, Depends
from sqlmodel import select, Session
from sqlalchemy import func
from app.db import get_session
from app.models import Hospital, PatientRequest
from .ws import manager
import json

router = APIRouter(prefix="/search", tags=["Search"])

# ✅ Helper broadcast for hospital search
async def broadcast_hospital_search(session: Session, query: str):
    stmt = select(Hospital).where(func.lower(Hospital.name).like(f"%{query.lower()}%"))
    results = session.exec(stmt).all()
    payload = {
        "type": "search_hospitals",
        "query": query,
        "results": [h.dict() for h in results]
    }
    await manager.broadcast(json.dumps(payload))

# ✅ Helper broadcast for patient request search
async def broadcast_request_search(session: Session, query: str):
    stmt = select(PatientRequest).where(func.lower(PatientRequest.requested_resource).like(f"%{query.lower()}%"))
    results = session.exec(stmt).all()
    payload = {
        "type": "search_requests",
        "query": query,
        "results": [r.dict() for r in results]
    }
    await manager.broadcast(json.dumps(payload))

# ✅ Normal REST search endpoint (Hospitals)
@router.get("/hospital")
def search_hospital(name: str, session: Session = Depends(get_session)):
    stmt = select(Hospital).where(func.lower(Hospital.name).like(f"%{name.lower()}%"))
    return session.exec(stmt).all()

# ✅ Normal REST search endpoint (Patient Requests)
@router.get("/requests")
def search_request(resource: str, session: Session = Depends(get_session)):
    stmt = select(PatientRequest).where(func.lower(PatientRequest.requested_resource).like(f"%{resource.lower()}%"))
    return session.exec(stmt).all()
