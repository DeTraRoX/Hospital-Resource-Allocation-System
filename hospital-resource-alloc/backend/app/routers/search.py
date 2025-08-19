from fastapi import APIRouter
from sqlmodel import Session, select
from ..db import engine
from ..models import Hospital, Request

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/hospital")
def search_hospital(name: str):
    with Session(engine) as session:
        result = session.exec(select(Hospital).where(Hospital.name.ilike(f"%{name}%"))).all()
        return result

@router.get("/requests")
def search_request(resource: str):
    with Session(engine) as session:
        result = session.exec(select(Request).where(Request.resource.ilike(f"%{resource}%"))).all()
        return result
