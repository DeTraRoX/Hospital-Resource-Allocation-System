from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from ..db import engine
from ..models import Allocation

router = APIRouter(prefix="/allocations", tags=["Allocations"])

@router.post("/", response_model=Allocation)
def create_allocation(allocation: Allocation):
    with Session(engine) as session:
        session.add(allocation)
        session.commit()
        session.refresh(allocation)
        return allocation

@router.get("/", response_model=list[Allocation])
def list_allocations():
    with Session(engine) as session:
        allocations = session.exec(select(Allocation)).all()
        return allocations
