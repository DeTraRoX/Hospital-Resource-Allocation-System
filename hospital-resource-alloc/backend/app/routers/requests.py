from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..db import engine
from ..models import Request

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.post("/", response_model=Request)
def create_request(req: Request):
    with Session(engine) as session:
        session.add(req)
        session.commit()
        session.refresh(req)
        return req

@router.get("/", response_model=list[Request])
def list_requests():
    with Session(engine) as session:
        reqs = session.exec(select(Request)).all()
        return reqs
